import pytest
import allure

from base import ApiBase
from consts import VK_EDC_LINK

@allure.epic("TestApi")
class TestApi(ApiBase):
    @allure.story("Create and delete segment")
    @pytest.mark.API
    def test_create_segment(self):
        with allure.step("Create segment"):
            segment_id = self.api_client.post_segment()  
        with allure.step("Check segment creation"):
            assert self.api_client.check_segment_creation(segment_id)
        with allure.step("Delete segment"):
            self.api_client.delete_segment(segment_id)
    
    @allure.story("Create and delete segment with source")
    @pytest.mark.API
    def test_create_segment_with_source(self):
        with allure.step("Get source id"):
            group_id = self.api_client.get_source(VK_EDC_LINK)
        with allure.step("Ad sorce"):
            source_id = self.api_client.post_source(group_id)
        with allure.step("Create segment with source"):
            segment_id = self.api_client.post_segment_with_source(group_id)
        with allure.step("Check segment with source creation"):
            assert self.api_client.check_segment_creation(segment_id)
        with allure.step("Delete segment with source"):
            self.api_client.delete_segment(segment_id)
        with allure.step("Delete source"):
            self.api_client.delete_source(source_id)
    
    @allure.story("Create and delete campaign")
    @pytest.mark.API
    def test_create_campaign(self, temp_image):
        with allure.step("Upload image"):
            image_id = self.api_client.post_image(temp_image)
        with allure.step("Create campaign"):
            campaign_id = self.api_client.post_camp(image_id)
        with allure.step("Check campaign creation"):
            assert self.api_client.check_campaign_creation(campaign_id)
        with allure.step("Delete campaign"):
            self.api_client.delete_campaign(campaign_id)
