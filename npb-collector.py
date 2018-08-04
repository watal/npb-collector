# -*- coding:utf-8 -*-

import collections as cl
import json
import time
import multiprocessing as mp
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

def scraping_npb():
    # チームの判別子を格納
    key_list = ["h","l","e","bs","f","m","c","t","db","g","d","s"]
    # 選手情報を格納するリスト
    players_list = []

    for team in key_list:
        # チーム毎のページ情報
        team_url = "http://npb.jp/bis/players/active/rst_" + team + ".html"
        # ページ情報を取得
        team_page = bs(urlopen(team_url), 'lxml')
        # ページ内の選手情報を取得
        players = team_page.find_all("a",class_='player_unit_1')

        for player in players:
            # 選手情報から個人ページのURLを取得
            links = player.get('href')
            player_url = 'http://npb.jp' + links
            player_page = bs(urlopen(player_url), 'lxml')

            # 1秒に1回実行
            time.sleep(1)
            div = player_page.find(id='pc_v_name')
            table = player_page.find(id='pc_bio')
            print(links)

            # コンテンツがあった場合，配列に追加
            if div != None:
                name = div.find('li', id='pc_v_name').text.strip('\n')
                if name != None:
                    # 各要素の抜き出し
                    position = table.find_all('td')[0].text.strip('\n')
                    toda = table.find_all('td')[1].text.strip('\n')
                    height_weight = table.find_all('td')[2].text.strip('\n')
                    born = table.find_all('td')[3].text.strip('\n')
                    career = table.find_all('td')[4].text.strip('\n')
                    draft = table.find_all('td')[5].text.strip('\n')

                    tmp_list = [{"team":div.find('li', id='pc_v_team').text.strip('\n')}]       # チーム名
                    tmp_list.append({"name":" ".join(name.split())})                            # 名前
                    tmp_list.append({"position":position.strip()})                              # ポジション
                    tmp_list.append({"toda":toda.strip()})                                      # 投打
                    tmp_list.append({"height_weight":height_weight.strip()})                    # 身長体重
                    tmp_list.append({"born":born.strip()})                                      # 生年月日
                    tmp_list.append({"career":career.strip()})                                  # 経歴
                    tmp_list.append({"draft":draft.strip()})                                    # ドラフト
                    players_list.append(tmp_list)

    # ファイル出力
    rslt_file = open('data/baseball_player'  + '.json', 'w')
    json.dump(players_list, rslt_file, ensure_ascii=False, indent=2)

if __name__=='__main__':
    scraping_npb()
