import requests
import json
import logging
from typing import List, Dict, Optional
from datetime import datetime

class ClinicalTrialsScraper:
    """
    Scraper for ClinicalTrials.gov API v2.0 to fetch AstraZeneca cell therapy trials
    """
    
    def __init__(self):
        self.base_url = "https://clinicaltrials.gov/api/v2/studies"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AstraZeneca-ClinicalTrials-Portal/1.0'
        })
    
    def fetch_astrazeneca_cell_therapy_trials(self, page_size: int = 1000) -> List[Dict]:
        """
        Fetch all AstraZeneca-related cell therapy trials
        
        Args:
            page_size: Number of results per page (max 1000)
            
        Returns:
            List of trial dictionaries with standardized structure
        """
        all_trials = []
        page_token = None
        
        try:
            while True:
                params = {
                    'query.intr': 'cell therapy OR gene therapy OR CAR-T OR adoptive cell transfer',
                    'query.spons': 'AstraZeneca',
                    'pageSize': page_size,
                    'format': 'json',
                    'countTotal': 'true'
                }
                
                if page_token:
                    params['pageToken'] = page_token
                
                logging.info(f"Fetching trials with params: {params}")
                response = self.session.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                studies = data.get('studies', [])
                
                if not studies:
                    break
                
                # Process and standardize each trial
                for study in studies:
                    processed_trial = self._process_trial_data(study)
                    if processed_trial:
                        all_trials.append(processed_trial)
                
                # Check for next page
                page_token = data.get('nextPageToken')
                if not page_token:
                    break
                
                logging.info(f"Fetched {len(studies)} trials, continuing to next page...")
        
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {str(e)}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error fetching trials: {str(e)}")
            return []
        
        # Also fetch trials where AstraZeneca is a collaborator
        collaborator_trials = self._fetch_collaborator_trials(page_size)
        all_trials.extend(collaborator_trials)
        
        # Remove duplicates based on NCT ID
        unique_trials = self._remove_duplicates(all_trials)
        
        logging.info(f"Total unique AstraZeneca cell therapy trials found: {len(unique_trials)}")
        return unique_trials
    
    def _fetch_collaborator_trials(self, page_size: int) -> List[Dict]:
        """Fetch trials where AstraZeneca is listed as collaborator"""
        trials = []
        page_token = None
        
        try:
            while True:
                params = {
                    'query.intr': 'cell therapy OR gene therapy OR CAR-T',
                    'query.term': 'AstraZeneca',  # General search for AstraZeneca mentions
                    'pageSize': page_size,
                    'format': 'json'
                }
                
                if page_token:
                    params['pageToken'] = page_token
                
                response = self.session.get(self.base_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                studies = data.get('studies', [])
                
                if not studies:
                    break
                
                # Filter for actual AstraZeneca involvement
                for study in studies:
                    if self._is_astrazeneca_involved(study):
                        processed_trial = self._process_trial_data(study)
                        if processed_trial:
                            trials.append(processed_trial)
                
                page_token = data.get('nextPageToken')
                if not page_token:
                    break
        
        except Exception as e:
            logging.error(f"Error fetching collaborator trials: {str(e)}")
        
        return trials
    
    def _is_astrazeneca_involved(self, study: Dict) -> bool:
        """Check if AstraZeneca is involved as sponsor or collaborator"""
        protocol = study.get('protocolSection', {})
        
        # Check sponsor
        sponsor_module = protocol.get('sponsorCollaboratorsModule', {})
        lead_sponsor = sponsor_module.get('leadSponsor', {})
        if 'astrazeneca' in lead_sponsor.get('name', '').lower():
            return True
        
        # Check collaborators
        collaborators = sponsor_module.get('collaborators', [])
        for collab in collaborators:
            if 'astrazeneca' in collab.get('name', '').lower():
                return True
        
        return False
    
    def _process_trial_data(self, study: Dict) -> Optional[Dict]:
        """
        Process and standardize trial data from API response
        
        Args:
            study: Raw study data from API
            
        Returns:
            Standardized trial dictionary or None if processing fails
        """
        try:
            protocol = study.get('protocolSection', {})
            
            # Basic identification
            identification = protocol.get('identificationModule', {})
            status = protocol.get('statusModule', {})
            design = protocol.get('designModule', {})
            sponsor_module = protocol.get('sponsorCollaboratorsModule', {})
            conditions_module = protocol.get('conditionsModule', {})
            interventions_module = protocol.get('interventionsModule', {})
            eligibility_module = protocol.get('eligibilityModule', {})
            contacts_module = protocol.get('contactsModule', {})
            
            # Extract key information
            trial_data = {
                # Core identifiers
                'nct_id': identification.get('nctId'),
                'brief_title': identification.get('briefTitle'),
                'official_title': identification.get('officialTitle'),
                'acronym': identification.get('acronym'),
                
                # Status information
                'overall_status': status.get('overallStatus'),
                'study_first_submitted_date': status.get('studyFirstSubmitDate'),
                'last_update_submitted_date': status.get('lastUpdateSubmitDate'),
                'start_date': status.get('startDateStruct', {}).get('date'),
                'primary_completion_date': status.get('primaryCompletionDateStruct', {}).get('date'),
                'completion_date': status.get('completionDateStruct', {}).get('date'),
                
                # Study design
                'study_type': design.get('studyType'),
                'phases': design.get('phases', []),
                'allocation': design.get('designInfo', {}).get('allocation'),
                'intervention_model': design.get('designInfo', {}).get('interventionModel'),
                'primary_purpose': design.get('designInfo', {}).get('primaryPurpose'),
                'masking': design.get('designInfo', {}).get('maskingInfo', {}).get('masking'),
                
                # Sponsor information
                'lead_sponsor': sponsor_module.get('leadSponsor', {}).get('name'),
                'lead_sponsor_class': sponsor_module.get('leadSponsor', {}).get('class'),
                'collaborators': [c.get('name') for c in sponsor_module.get('collaborators', [])],
                
                # Conditions and interventions
                'conditions': conditions_module.get('conditions', []),
                'interventions': [
                    {
                        'type': intervention.get('type'),
                        'name': intervention.get('name'),
                        'description': intervention.get('description')
                    } for intervention in interventions_module.get('interventions', [])
                ],
                
                # Eligibility
                'eligibility_criteria': eligibility_module.get('eligibilityCriteria'),
                'healthy_volunteers': eligibility_module.get('healthyVolunteers'),
                'gender': eligibility_module.get('sex'),
                'minimum_age': eligibility_module.get('minimumAge'),
                'maximum_age': eligibility_module.get('maximumAge'),
                
                # Contact information
                'locations': self._extract_locations(contacts_module),
                'central_contacts': contacts_module.get('centralContacts', []),
                
                # Additional metadata
                'enrollment': design.get('enrollmentInfo', {}).get('count'),
                'keywords': protocol.get('conditionsModule', {}).get('keywords', []),
                'brief_summary': protocol.get('descriptionModule', {}).get('briefSummary'),
                'detailed_description': protocol.get('descriptionModule', {}).get('detailedDescription'),
                
                # API metadata
                'last_scraped': datetime.now().isoformat(),
                'raw_data': study  # Store complete raw data for detailed view
            }
            
            return trial_data
            
        except Exception as e:
            logging.error(f"Error processing trial data: {str(e)}")
            return None
    
    def _extract_locations(self, contacts_module: Dict) -> List[Dict]:
        """Extract and format location information"""
        locations = []
        location_contacts = contacts_module.get('locations', [])
        
        for location in location_contacts:
            facility = location.get('facility', {})
            location_data = {
                'facility_name': facility.get('name'),
                'city': facility.get('city'),
                'state': facility.get('state'),
                'zip_code': facility.get('zip'),
                'country': facility.get('country'),
                'status': location.get('status'),
                'contacts': location.get('contacts', [])
            }
            locations.append(location_data)
        
        return locations
    
    def _remove_duplicates(self, trials: List[Dict]) -> List[Dict]:
        """Remove duplicate trials based on NCT ID"""
        seen_nct_ids = set()
        unique_trials = []
        
        for trial in trials:
            nct_id = trial.get('nct_id')
            if nct_id and nct_id not in seen_nct_ids:
                seen_nct_ids.add(nct_id)
                unique_trials.append(trial)
        
        return unique_trials
    
    def fetch_trial_details(self, nct_id: str) -> Optional[Dict]:
        """
        Fetch detailed information for a specific trial
        
        Args:
            nct_id: NCT identifier for the trial
            
        Returns:
            Detailed trial information or None if not found
        """
        try:
            url = f"{self.base_url}/{nct_id}"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            study = data.get('protocolSection', {})
            
            if study:
                return self._process_trial_data({'protocolSection': study})
            else:
                logging.error(f"No data found for trial {nct_id}")
                return None
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch details for {nct_id}: {str(e)}")
            return None
    
    def search_cell_therapy_trials(self, additional_filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for cell therapy trials with additional filters
        
        Args:
            additional_filters: Dictionary of additional search parameters
            
        Returns:
            List of matching trials
        """
        params = {
            'query.intr': 'cell therapy OR gene therapy OR CAR-T',
            'pageSize': 1000,
            'format': 'json'
        }
        
        if additional_filters:
            params.update(additional_filters)
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            studies = data.get('studies', [])
            
            trials = []
            for study in studies:
                processed_trial = self._process_trial_data(study)
                if processed_trial:
                    trials.append(processed_trial)
            
            return trials
            
        except Exception as e:
            logging.error(f"Search failed: {str(e)}")
            return []

# Global scraper instance
scraper = ClinicalTrialsScraper()