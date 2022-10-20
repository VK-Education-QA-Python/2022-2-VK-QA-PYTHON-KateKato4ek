import pytest

from base import BaseCase
from ui.fixtures import temp_image

class TestCampaignPage(BaseCase):
    @pytest.mark.UI
    def test_create_new_campaign(self, temp_image):
        campaign_page = self.dashboard_page.get_campaign_page()
        campaign_page.create_new_campaign(temp_image)
        
        assert campaign_page.is_campaign_created()
        
        campaign_page.delete_campaign_page()

class TestAudiencesPage(BaseCase):
    @pytest.mark.UI
    def test_create_segment(self):
        audience_page = self.dashboard_page.get_audience_page()
        audience_page.create_segment()
        
        assert audience_page.is_segment_created()
        
        audience_page.delete_segment()
    
    @pytest.mark.UI
    def test_create_segment_with_link(self):
        audience_page = self.dashboard_page.get_audience_page()
        audience_page.add_source()
        self.dashboard_page.go_to_audience_page()
        audience_page.create_segment_with_link()
        
        assert audience_page.is_segment_created()
        
        audience_page.delete_segment()
        audience_page.delete_source()
