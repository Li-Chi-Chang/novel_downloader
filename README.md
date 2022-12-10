# novel_downloader

For my wife

## Install

1. pip install -r requirements.txt
2. pip install -r gmail_sending/requirements.txt
3. pip install -r web_browser/requirements.txt

## Add a site

1. go to novelSitesSetting.csv
2. Add CSS selector and url and note for it.
3. if need more clearify, specify "Y", otherwise, "N".
4. if need more clearify, code the clear function in siteCustomClearify.py

## Download

1. add start url and end url to def scope.
2. run python download.py

## available features

1. javascript rendered sites (ALL)
2. ~~self defined callback for each sites (# not available now)~~

## my notes

* add submodule

    ```cmd
    git submodule add git@github.com:Li-Chi-Chang/web_browser.git book_reader/web_browser
    ```

* pull with submodule

    ```cmd
    git clone --recursive https://github.com/Li-Chi-Chang/novel_downloader.git
    ```

* change submodule path

https://stackoverflow.com/questions/913701/how-to-change-the-remote-repository-for-a-git-submodule/19126528
https://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule
https://stackoverflow.com/questions/9035895/how-do-i-add-a-submodule-to-a-sub-directory

* python virtual env

    ```cmd
    virtualenv .
    source ./bin/activate
    ```

* simplify <-> traditional

https://yanwei-liu.medium.com/python自然語言處理-四-繁簡轉換利器opencc-74021cbc6de3