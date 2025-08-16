from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from tqdm import tqdm


def select_location(page, opt):
    # ul.ul_select 안에서 text 일치하는 a 태그 직접 찾기
    locator = page.locator(f"ul.ul_select >> :text-is('{opt['text']}')")

    # 강제로 스크롤해서 중앙에 오게 하기 (scroll_into_view_if_needed 대체)
    locator.evaluate("el => el.scrollIntoView({block: 'center'})")

    page.wait_for_timeout(1500)
    locator.click(force=True)
    print(opt)
    page.wait_for_timeout(1500)


def search_and_expand_all(page):
    # 검색하기 버튼 클릭
    page.click("button#storeSearch")
    page.wait_for_timeout(2000)

    # 더보기 버튼이 사라질 때까지 반복 클릭
    while True:
        try:
            more_btn = page.locator("a#moreData")
            if more_btn.is_visible():
                more_btn.click()
                page.wait_for_timeout(1500)
            else:
                break
        except Exception:
            break


def collect_store_data(page):
    store_data = []
    rows = page.locator("tbody#resultList > tr")
    row_count = rows.count()

    for i in range(row_count):
        row = rows.nth(i)
        cells = row.locator("td")
        업종 = cells.nth(0).text_content().strip()
        가맹점 = cells.nth(1).text_content().strip()
        주소 = cells.nth(2).text_content().strip()

        store_data.append(
            {
                "업종": 업종,
                "가맹점": 가맹점,
                "주소": 주소,
            }
        )

    return store_data


with sync_playwright() as p:
    browswer = p.chromium.launch(headless=False, slow_mo=100)
    page = browswer.new_page()

    # Please input your crawling web site and Change the code selector about the website you want to crawl.
    page.goto("YOUR CRAWLING WEB SITE")
    page.wait_for_timeout(1500)

    si_options = page.eval_on_selector_all(
        "select#searchSido > option",
        "options => options.map(option => ({ value: option.value, text: option.textContent.trim() }))",
    )
    for si_option in tqdm(si_options[1:]):
        page.click("a.btn_select[title='시/도 선택']")
        page.wait_for_timeout(1500)
        select_location(page, si_option)

        si_gu_gun_options = page.eval_on_selector_all(
            "select#ajaxView_Sigungu > option",
            "options => options.map(option => ({ value: option.value, text: option.textContent.trim() }))",
        )
        page.wait_for_timeout(1500)
        for si_gu_gun_option in tqdm(si_gu_gun_options[13:14]):
            page.click("a.btn_select[title='구/군 선택 선택 값']")
            page.wait_for_timeout(1500)
            select_location(page, si_gu_gun_option)

            dong_options = page.eval_on_selector_all(
                "select#ajaxView_Dong > option",
                "options => options.map(option => ({ value: option.value, text: option.textContent.trim() }))",
            )
            for dong_option in tqdm(dong_options[8:10]):
                page.click("a.btn_select[title='읍/면/동 선택 선택 값']")
                page.wait_for_timeout(1500)
                select_location(page, dong_option)

                # 검색하기 & 더보기 클릭
                search_and_expand_all(page)

                # Data 파싱
                store_list = collect_store_data(page)

                # JSON 저장
                import json

                fname = f"{si_option['text']}_{si_gu_gun_option['text']}_{dong_option['text']}.json"

                with open(fname, "w", encoding="utf-8") as f:
                    json.dump(store_list, f, ensure_ascii=False, indent=2)
                    print(f"{dong_option['text']} 완료")
                page.wait_for_timeout(1500)
            print(f"{si_gu_gun_option['text']} 완료")
            page.wait_for_timeout(1500)
        print(f"{si_option['text']} 완료")
        page.wait_for_timeout(1500)

    page.wait_for_timeout(1500)
