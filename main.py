from utils.settings import update_chrome, open_page
from utils.clicks import click_elements

if __name__ == "__main__":
    driver = update_chrome()
    open_page('https://apply.lh.or.kr/lhapply/apply/wt/wrtanc/selectWrtancList.do?mi=1026')
    click_elements(driver)
    driver.quit()