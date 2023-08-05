# Facebook_Crawler
The project is developed by Teng-Lin Yu(游騰林). If you have any questions or suggestions, please feel free to contact me. 

## Support

[![ecgo.png](https://raw.githubusercontent.com/TLYu0419/facebook_crawler/main/images/ecgo.png)](https://payment.ecpay.com.tw/QuickCollect/PayData?GcM4iJGUeCvhY%2fdFqqQ%2bFAyf3uA10KRo%2fqzP4DWtVcw%3d)


Web crawler projects need much time to maintain and developed. If you could support me, I will really appreciate it. Either donate, star or share is good for me. Your support will help me develop more functions, such as a database, GUI interface, or any other possibilities(You can write an e-mail and share your thoughts with me.) 

網路爬蟲專案會需要花費相當多時間來維護和開發。如果你能支持我我會非常感謝。不論是捐助、給星星或跟朋友分享對我來說都是非常好的支持方式。你的支持會是我繼續開發這個專案的動力，例如建立資料庫、圖形界面或其他任何的可能(歡迎寫信給我並跟我分享你的想法)

## What's this?

The project could help us collect data from Facebook's public Fanspage / group. Here are the three big points of this project: 
1. You don't need to log in to your account.
2. Easy to use: Just key in the Fanspage/group URL and the target date. 
3. Efficiently: It collects the data through request directly instead of Selenium.


這個專案可以幫我們從 Facebook 公開的的粉絲頁和公開社團收集資料。以下是本專案的 3 個重點:
1. 不需要登入你的帳號
2. 使用簡易: 僅需輸入網址與指定的日期(藉此跳出迴圈)
3. 非常有效率: 透過 requests 直接抓取資料，不需透過 Selenium

## Quickstart
- Install Method
  ```pip
  pip install facebook-crawler
  ```

- Facebook Fanspage 
  ```python
  import facebook_crawler
  pageurl= 'https://www.facebook.com/diudiu333'
  facebook_crawler.Crawl_PagePosts(pageurl=pageurl, until_date='2021-01-01')
  ```
  ![quickstart_fanspage.png](https://raw.githubusercontent.com/TLYu0419/facebook_crawler/main/images/quickstart_fanspage.png)
- Group
  ```python
  import facebook_crawler
  groupurl = 'https://www.facebook.com/groups/pythontw'
  facebook_crawler.Crawl_GroupPosts(groupurl, until_date='2021-01-01')
  ```
  ![quickstart_group.png](https://raw.githubusercontent.com/TLYu0419/facebook_crawler/main/images/quickstart_group.png)
## License
- [Apache License 2.0](./LiCENSE)
- 本專案提供的所有內容均用於教育、非商業用途。本專案不對資料內容錯誤、更新延誤或傳輸中斷負任何責任。

## Contact
- Email: tlyu0419@gmail.com
- Any suggestions is good and feel free to contact me.


## To Do
- GUI interface
- Database

