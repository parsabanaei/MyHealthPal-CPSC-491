import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import asyncio

try:
    from google.cloud import firestore
    from google.auth import default
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirestoreService:
    """
    Firestore database service for MyHealthPal
    
    Handles all database operations including:
    - Storing health assessments
    - Retrieving assessment data
    - Updating assessment records
    - Managing user data
    """
    
    def __init__(self):
        """Initialize Firestore service"""
        self.db = None
        self.collection_name = "health_assessments"
        self.connected = False
        
        self._initialize_firestore()
    
    def _initialize_firestore(self):
        """Initialize Firestore client"""
        try:
            if not FIRESTORE_AVAILABLE:
                logger.warning("Firestore client not available - using mock mode")
                self.connected = False
                return
            
            # Initialize Firestore client
            # In Cloud Run, this will automatically use the service account
            # For local development, you may need to set GOOGLE_APPLICATION_CREDENTIALS
            self.db = firestore.Client()
            self.connected = True
            logger.info("Firestore client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firestore: {e}")
            self.connected = False
    
    async def save_assessment(self, assessment_data: Dict[str, Any]) -> bool:
        """
        Save a health assessment to Firestore
        
        Args:
            assessment_data: Complete assessment data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.connected:
                logger.info("Mock: Would save assessment to Firestore")
                return True
            
            # Use the assessment ID as the document ID
            doc_id = assessment_data.get('id')
            if not doc_id:
                raise ValueError("Assessment data must include an 'id' field")
            
            # Add server timestamp
            assessment_data['server_timestamp'] = firestore.SERVER_TIMESTAMP
            
            # Save to Firestore
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.set(assessment_data)
            
            logger.info(f"Assessment {doc_id} saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving assessment: {e}")
            return False
    
    async def get_assessment(self, assessment_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a health assessment by ID
        
        Args:
            assessment_id: Unique assessment identifier
            
        Returns:
            Assessment data dictionary or None if not found
        """
        try:
            if not self.connected:
                # Return mock data for testing
                logger.info(f"Mock: Would retrieve assessment {assessment_id}")
                return self._get_mock_assessment(assessment_id)
            
            doc_ref = self.db.collection(self.collection_name).document(assessment_id)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                logger.info(f"Assessment {assessment_id} retrieved successfully")
                return data
            else:
                logger.warning(f"Assessment {assessment_id} not found")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving assessment {assessment_id}: {e}")
            return None
    
    async def update_assessment(self, assessment_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update specific fields in a health assessment
        
        Args:
            assessment_id: Unique assessment identifier
            update_data: Dictionary with fields to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.connected:
                logger.info(f"Mock: Would update assessment {assessment_id}")
                return True
            
            # Add server timestamp to update
            update_data['server_timestamp'] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection(self.collection_name).document(assessment_id)
            doc_ref.update(update_data)
            
            logger.info(f"Assessment {assessment_id} updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error updating assessment {assessment_id}: {e}")
            return False
    
    async def get_assessments_by_email(self, email: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve assessments for a specific email address
        
        Args:
            email: User email address
            limit: Maximum number of assessments to retrieve
            
        Returns:
            List of assessment dictionaries
        """
        try:
            if not self.connected:
                logger.info(f"Mock: Would retrieve assessments for {email}")
                return [self._get_mock_assessment("mock-id")]
            
            # Query assessments by email, ordered by timestamp
            query = (self.db.collection(self.collection_name)
                    .where('user_email', '==', email)
                    .order_by('timestamp', direction=firestore.Query.DESCENDING)
                    .limit(limit))
            
            docs = query.stream()
            assessments = []
            
            for doc in docs:
                assessment_data = doc.to_dict()
                assessments.append(assessment_data)
            
            logger.info(f"Retrieved {len(assessments)} assessments for {email}")
            return assessments
            
        except Exception as e:
            logger.error(f"Error retrieving assessments for {email}: {e}")
            return []
    
    async def delete_assessment(self, assessment_id: str) -> bool:
        """
        Delete a health assessment (for privacy compliance)
        
        Args:
            assessment_id: Unique assessment identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.connected:
                logger.info(f"Mock: Would delete assessment {assessment_id}")
                return True
            
            doc_ref = self.db.collection(self.collection_name).document(assessment_id)
            doc_ref.delete()
            
            logger.info(f"Assessment {assessment_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting assessment {assessment_id}: {e}")
            return False
    
    async def get_assessment_stats(self) -> Dict[str, Any]:
        """
        Get aggregated statistics about assessments
        
        Returns:
            Dictionary with statistics
        """
        try:
            if not self.connected:
                logger.info("Mock: Would retrieve assessment statistics")
                return {
                    'total_assessments': 42,
                    'total_users': 38,
                    'assessments_today': 5,
                    'avg_bmi': 24.8,
                    'risk_distribution': {
                        'low': 15,
                        'medium': 20,
                        'high': 7
                    }
                }
            
            # This would require aggregation queries in a real implementation
            # For now, return basic count
            collection_ref = self.db.collection(self.collection_name)
            docs = collection_ref.stream()
            
            total_count = sum(1 for _ in docs)
            
            return {
                'total_assessments': total_count,
                'collection_name': self.collection_name,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error retrieving statistics: {e}")
            return {}
    
    def _get_mock_assessment(self, assessment_id: str) -> Dict[str, Any]:
        """
        Generate mock assessment data for testing
        
        Args:
            assessment_id: Assessment ID to include in mock data
            
        Returns:
            Mock assessment data
        """
        return {
            'id': assessment_id,
            'user_email': 'test@example.com',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'input_data': {
                'age': 35,
                'gender': 'Male',
                'height_cm': 175.0,
                'weight_kg': 80.0,
                'activity_level': 'Moderate',
                'family_history': False,
                'smoking': False
            },
            'results': {
                'bmi': 26.1,
                'bmi_category': 'Overweight',
                'obesity_risk': 'Medium',
                'heart_disease_risk': 'Low'
            },
            'report_sent': True,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check Firestore service health
        
        Returns:
            Health status dictionary
        """
        try:
            if not self.connected:
                return {
                    'status': 'disconnected',
                    'firestore_available': FIRESTORE_AVAILABLE,
                    'mode': 'mock'
                }
            
            # Try a simple read operation
            collection_ref = self.db.collection(self.collection_name)
            # Just check if we can access the collection
            list(collection_ref.limit(1).stream())
            
            return {
                'status': 'healthy',
                'firestore_available': True,
                'collection': self.collection_name,
                'mode': 'production'
            }
            
        except Exception as e:
            logger.error(f"Firestore health check failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'firestore_available': FIRESTORE_AVAILABLE,
                'mode': 'error'
            }
    
    def set_mock_mode(self, mock: bool = True):
        """
        Enable or disable mock mode for testing
        
        Args:
            mock: True to enable mock mode, False to use real Firestore
        """
        if mock:
            self.connected = False
            logger.info("Firestore service set to mock mode")
        else:
            self._initialize_firestore()
            logger.info("Firestore service set to production mode")
    
    async def batch_save_assessments(self, assessments: List[Dict[str, Any]]) -> int:
        """
        Save multiple assessments in a batch operation
        
        Args:
            assessments: List of assessment data dictionaries
            
        Returns:
            Number of successfully saved assessments
        """
        if not self.connected:
            logger.info(f"Mock: Would batch save {len(assessments)} assessments")
            return len(assessments)
        
        try:
            batch = self.db.batch()
            success_count = 0
            
            for assessment_data in assessments:
                doc_id = assessment_data.get('id')
                if doc_id:
                    doc_ref = self.db.collection(self.collection_name).document(doc_id)
                    assessment_data['server_timestamp'] = firestore.SERVER_TIMESTAMP
                    batch.set(doc_ref, assessment_data)
                    success_count += 1
            
            batch.commit()
            logger.info(f"Batch saved {success_count} assessments")
            return success_count
            
        except Exception as e:
            logger.error(f"Error in batch save: {e}")
            return 0 