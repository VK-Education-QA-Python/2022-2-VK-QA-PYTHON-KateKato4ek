import pytest
import allure

from base import BaseCase
from ui.fixtures import temp_image

@allure.epic("Campaign Page")
class TestCampaignPage(BaseCase):
    @allure.story("Checking creating new campaign")
    @pytest.mark.UI
    def test_create_new_campaign(self, temp_image):
        with allure.step("Get campaign page"):
            campaign_page = self.dashboard_page.get_campaign_page()
        with allure.step("Create campaign"):    
            campaign_page.create_new_campaign(temp_image)
        with allure.step("Is campaign created?"):
            assert campaign_page.is_campaign_created()
        with allure.step("Delte campaign"):
            campaign_page.delete_campaign_page()

@allure.epic("Audiences Page")
class TestAudiencesPage(BaseCase):
    @allure.story("Checking creating new segment")
    @pytest.mark.UI
    def test_create_segment(self):
        with allure.step("Get audience page"):
            audience_page = self.dashboard_page.get_audience_page()
        with allure.step("Create segment"):
            audience_page.create_segment()
        with allure.step("Is segment created?"):
            assert audience_page.is_segment_created()
        with allure.step("Delete segment"):
            audience_page.delete_segment()
    
    @allure.story("Checking creating new segment with link")      
    @pytest.mark.UI
    def test_create_segment_with_link(self):
        with allure.step("Get audience page"):
            audience_page = self.dashboard_page.get_audience_page()
        with allure.step("Add source"):
            audience_page.add_source()
        with allure.step("Get audience page"):   
            self.dashboard_page.go_to_audience_page()
        with allure.step("Create audience page with link"):    
            audience_page.create_segment_with_link()
        with allure.step("Is segment with libk created?"):
            assert audience_page.is_segment_created()
        with allure.step("Delete segment with link"):
            audience_page.delete_segment()
        with allure.step("Delete source"):
            audience_page.delete_source()
