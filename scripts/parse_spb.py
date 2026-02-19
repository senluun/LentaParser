"""
Скрипт для получения каталога товаров Ленты для Санкт-Петербурга.

Этот скрипт выполняет запрос к API Ленты для получения списка товаров
из определенной категории для магазинов в Санкт-Петербурге.
Результат сохраняется в файл sbp_result.json.
"""

import requests
import json
import os
from pathlib import Path

# Определяем путь к корневой папке проекта (на уровень выше scripts/)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Создаем папку data, если её нет
DATA_DIR.mkdir(exist_ok=True)

# URL эндпоинта API для получения товаров каталога
url = "https://api.lenta.com/v1/catalog/items"

# Заголовки запроса, имитирующие мобильное приложение Android
headers = {
    "Accept-Encoding": "gzip",
    "ADID": "cc8ca939acd905af1e05885bcf5d6040",
    "AdvertisingId": "4131b7c3-8d3b-47fe-bea4-4d6f7154f03e",
    "App-Version": "6.72.0",
    "Client": "android_16_6.72.0_rustore",
    "Connection": "Keep-Alive",
    "Content-Type": "application/json; charset=utf-8",
    "DeviceId": "A-c0cfefb0-505c-42f5-b88b-f0839a532cc9",
    "Experiments": "exp_recommendation_cms.false,exp_lentapay.test,exp_profile_bell.test,exp_cl_omni_authorization.test,exp_fullscreen.test,exp_onboarding_editing_order.test,exp_cart_new_carousel.default,exp_sbp_enabled.test,exp_profile_settings_email.default,exp_cl_omni_refusalprintreceipts.test,exp_search_suggestions_popular_sku.default,exp_cl_new_csi.test,exp_cl_new_csat.default,exp_delivery_price_info.test,exp_interval_jump.test,exp_cardOne_promo_type.test,exp_birthday_coupon_skus.test,exp_qr_cnc.test,exp_where_place_cnc.test,exp_editing_cnc_onboarding.test,exp_editing_cnc.test,exp_pickup_in_delivery.test,exp_welcome_onboarding.control,exp_where_place_new.default,exp_start_page.test,exp_default_payment_type.default,exp_start_page_onboarding.default,exp_search_new_logic.default,exp_referral_program_type.default,exp_new_action_pages.test,exp_items_by_rating.test,exp_can_accept_early.default,exp_online_subscription.test,exp_hide_cash_payment_for_cnc_wo_adult_items.default,exp_prices_per_quantum.test,exp_web_chips_online.default,exp_chips_online.test,exp_promo_without_benefit.default,exp_cart_forceFillDelivery.default,exp_banner_sbp_checkout_step_3.default,exp_badge_sbp_checkout_step_3.test_B,exp_kit_banner_sbp_checkout_step_3.default,exp_kit_badge_sbp_checkout_step_3.default,exp_profile_stories.test,exp_cl_new_ui_csi_comment.comment,exp_in_app_update.default,exp_sorting_catalog.default,exp_aa_test_2025_04.default,exp_search_items_by_date.test_b,exp_product_page_by_blocks.test,exp_without_a_doorbell.test_A,exp_without_a_doorbell_new.default,exp_edit_payment_type.test,exp_edit_payment_type_new.default,exp_search_photo_positions.test,exp_new_matrix.test,exp_another_button_ch.default,exp_progressbar_and_title.test,exp_auto_fill_coupon.test,exp_promo_and_bonus.test,exp_about_cnc_optimization.default,exp_online_categories.default,exp_no_intervals.default,exp_web_b2b_excel_load.default,exp_cart_save_with_promo.test,exp_email_optional_full_registration.default,exp_cl_new_rateapp.default,exp_similar_goods_cart.test,exp_cart_redesign_promocode.default,exp_search_new_filters.test,exp_loyalty_categories_labels.default,exp_search_multicard.test,exp_delivery_promocode_bd_coupon.default,exp_search_disable_fuzziness.default,exp_ui_catalog_level_2.test,exp_fullscreen_inapp_vs_native.test1,exp_search_collections_ranking.test,exp_search_elastic_tokens.default,exp_cl_new_tapbar.default,exp_cl_new_tapbar_tab.default,exp_search_my_choice_stock_priority.test_b,exp_cart_free_sample.default,exp_about_promocode.test_A,exp_personal_promo_detail_for_delivery.test_2,exp_search_combined_field.default,exp_search_unified.default,exp_web_personal_promo_detail_for_delivery.default,exp_web_personal_promo_delivery_chips.default,exp_b2b_web_mob_checkout.default,exp_personal_promo_delivery_chips.test,exp_ds_cnc_pers_recom.test,exp_ds_mntk_pers_recom.default,exp_shopping_statistics.default,exp_pin_create_button.default,exp_search_ui_catalog_pim.test,exp_search_video.default,exp_search_pinned_reviews.test,exp_sbp_instead_of_lenta_pay.test_1,exp_card1_start_page.default,exp_status_assemble_completed.test,exp_cl_new_ui_csi_comment2.test,exp_online_subscription_discount.control,exp_start_page_button_notifications.test,exp_quick_checkout.default,exp_quick_checkout_update.default,exp_search_no_stock.true,exp_main_page_new_mode_shop.test,exp_brief_description_promo.default,exp_new_offer_new_user_v1.default,exp_order_feedback_show.test,exp_leave_order_at_door.test,exp_leave_order_at_door_new.test,exp_search_quantity_discount_promo.test,exp_start_page_button_navigation_off.default,exp_obi_webview.true,exp_huawei_adjust_new_tokens.true,exp_import_goods_in_basket.efault,exp_unpin_tabbar.default,exp_mna_orders_editing.default,exp_consent.default,exp_main_stories.test,exp_from_store_myself.default,exp_new_bs_catalog_startpage.test,exp_be_soon_show_explain_message.test,exp_startpage_mainpage_new_address_design.default,exp_bubble_discount_startpage_mainpage.default,exp_startpage_zone_description.default,exp_samenamespace_check_1.true,exp_samenamespace_check_2.true,exp_ds_pd_carousel.test,exp_ds_pers_recom_delivery_2.test,exp_search_ds_catboost_2.control,exp_new_user_promo_profile.default,exp_novikov_test.OFF,exp_order_created_action_banner.test,exp_ds_mntk_pers_cat.default,exp_search_ds_empty_recom.test,exp_badges_pers_cashback.control,exp_hit_price_timer.test,exp_temp_exp_ds_pd_carousel_a.false,exp_temp_exp_ds_pd_carousel_b.false,exp_temp_exp_ds_pd_carousel_android.default,exp_temp_exp_ds_pd_carousel_android_general.default,exp_temp_samesplit_check_f.a,exp_interval_jump_30.test,exp_temp_exp_ds_pd_carousel_ios_general.default,exp_search_purchased_badge.default,exp_pwa_cart.default,exp_pwa_checkout.default,exp_auto_detection_store_for_new_user.default,exp_return_available_items.default,exp_b2c_onboarding_send_cart.default,exp_b2b_send_cart.default,exp_b2c_send_cart.default,exp_cart_item_modify_version20.default,exp_auth_sber_id.default,exp_search_voice_search_ai.default,exp_startpage_redesign_qr_and_loy.default,exp_web_aa_2026_01_v1.default,exp_startpage_redesign_missions.default,exp_search_pdp_big_photo.default,exp_startpage_tab_shop_on_the_map.test,exp_startpage_logics_button_pickup.default,exp_open_screen_card1_profile_without_address.default,exp_web_cancel_to_edit_cnc.default,exp_ch_how_much_unit.default,exp_search_fd.default,exp_authorization_tg.default,exp_ds_cat_diversity.test,exp_more_about_price.default,exp_br_1521_refresh_auth_token.default,exp_kpp_aa.default,exp_unpin_tabbar_v2.default,exp_b2c_bot_web_send_cart.default,exp_nearest_hubs_new_logic.default,exp_new_bs_catalog_startpage_v2.default,exp_favorite_categories_description.default",
    "Host": "api.lenta.com",
    "LocalTime": "2026-02-19T21:02:36.596399Z",
    "Qrator-Token": "2cb4b1151a492918fc75ad8d333747ea",
    "SessionToken": "CC5DD8D5B6AF243E80E5254B8847D9D0",
    "Timestamp": "1771534956",
    "User-Agent": "lo, 6.72.0",
    "X-Delivery-Mode": "pickup",
    "X-Device-Brand": "google",
    "X-Device-ID": "A-c0cfefb0-505c-42f5-b88b-f0839a532cc9",
    "X-Device-Name": "Google",
    "X-Device-OS": "Android",
    "X-Device-OS-Version": "36",
    "X-Organization-ID": "",
    "X-Platform": "omniapp",
    "X-Retail-Brand": "lo",
}

# Тело запроса с параметрами фильтрации и сортировки
payload = {
    "categoryId": 4,  # ID категории товаров (4 - основная категория)
    "filters": {
        "multicheckbox": [],  # Фильтры с множественным выбором (не используются)
        "checkbox": [],       # Чекбокс фильтры (не используются)
        "range": []           # Диапазонные фильтры, например, по цене (не используются)
    },
    "sort": {
        "type": "popular",    # Тип сортировки: по популярности
        "order": "desc"       # Порядок сортировки: по убыванию
    },
    "limit": 100,  # Максимальное количество товаров в ответе (увеличено до 100)
    "offset": 0,   # Смещение для пагинации (начинаем с первого товара)
}

# Выполняем POST запрос к API
response = requests.post(url, headers=headers, json=payload)

print(f"Status: {response.status_code}")

# Обрабатываем ответ
if response.status_code == 200:
    data = response.json()
    
    # Сохраняем полученные данные в JSON файл
    output_file = DATA_DIR / "spb_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Результат сохранен в {output_file}")
else:
    print(f"Ошибка: {response.text}")