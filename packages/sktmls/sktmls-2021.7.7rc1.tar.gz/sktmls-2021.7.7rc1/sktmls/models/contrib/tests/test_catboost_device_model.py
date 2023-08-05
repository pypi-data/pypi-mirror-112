import pytest

import numpy as np

from catboost import CatBoostClassifier

from sktmls.meta_tables import MetaTable
from sktmls.models.contrib import CatboostDeviceModel


class TestCatboostDeviceModel:
    @pytest.fixture(scope="class")
    def param(self):
        return {
            "model": CatboostDeviceModel(
                model=CatBoostClassifier(),
                model_name="test_model",
                model_version="test_version",
                model_features=["eqp_mdl_cd", "age"] + ["feature1", "feature2", "feature3", "feature4"],
                default_model_feature_values=[0.0, "N", 10.0, "S"],
                target_prod_id=["000001153", "000004632", "000004795", "000004794"],
                products={
                    "000004794": {
                        "name": "iPhone 12 Pro Max",
                        "type": "device",
                        "context_features": ["context_age10", "context_age20"],
                        "random_context": False,
                    },
                },
                products_meta={
                    "000001153": {"product_grp_nm": "갤럭시 S7 엣지", "mfact_nm": "삼성전자", "eqp_mdl_ntwk": "4G"},
                    "000004632": {"product_grp_nm": "갤럭시 Z 플립 5G", "mfact_nm": "삼성전자", "eqp_mdl_ntwk": "5G"},
                    "000004795": {"product_grp_nm": "iPhone 12 mini", "mfact_nm": "Apple", "eqp_mdl_ntwk": "5G"},
                    "000004794": {"product_grp_nm": "iPhone 12 Pro Max", "mfact_nm": "Apple", "eqp_mdl_ntwk": "5G"},
                },
                device_meta=MetaTable(
                    **{
                        "id": 1,
                        "name": "name",
                        "description": "desc",
                        "schema": {},
                        "items": [
                            {
                                "name": "SS90",
                                "values": {
                                    "product_grp_id": "000001153",
                                    "product_grp_nm": "갤럭시 S7 엣지",
                                    "rep_eqp_mdl_cd": "SS30",
                                    "rep_eqp_yn": "N",
                                    "mfact_nm": "삼성전자",
                                    "color_hex": "N/A",
                                    "color_nm": "N/A",
                                    "network_type": "4G",
                                },
                            },
                            {
                                "name": "A266",
                                "values": {
                                    "product_grp_id": "000004632",
                                    "product_grp_nm": "갤럭시 Z 플립 5G",
                                    "rep_eqp_mdl_cd": "A266",
                                    "rep_eqp_yn": "Y",
                                    "mfact_nm": "삼성전자",
                                    "color_hex": "525453",
                                    "color_nm": "미스틱 그레이",
                                    "network_type": "5G",
                                },
                            },
                            {
                                "name": "A2FY",
                                "values": {
                                    "product_grp_id": "000004795",
                                    "product_grp_nm": "iPhone 12 mini",
                                    "rep_eqp_mdl_cd": "A2FY",
                                    "rep_eqp_yn": "Y",
                                    "mfact_nm": "Apple",
                                    "color_hex": "312E37",
                                    "color_nm": "블랙",
                                    "network_type": "5G",
                                },
                            },
                            {
                                "name": "A2GU",
                                "values": {
                                    "product_grp_id": "000004794",
                                    "product_grp_nm": "iPhone 12 Pro Max",
                                    "rep_eqp_mdl_cd": "A2GT",
                                    "rep_eqp_yn": "Y",
                                    "mfact_nm": "Apple",
                                    "color_hex": "E6E7E2",
                                    "color_nm": "실버",
                                    "network_type": "5G",
                                },
                            },
                        ],
                        "user": "user",
                        "created_at": "1",
                        "updated_at": "1",
                    }
                ),
                num_pick=3,
            )
        }

    def test_000_generic_context_apple(self, param, mocker):
        mocker.patch("catboost.CatBoostClassifier.predict_proba", return_value=np.array([0.1, 3.4, 1.0, 3.3]))

        assert param.get("model").predict(["A2FY", 25, 0.0, "N", 10.0, "S"])["items"][0] == {
            "id": "000004794",
            "name": "iPhone 12 Pro Max",
            "props": {"context_id": "context_age20", "network_type": "5G"},
            "type": "device",
        }
