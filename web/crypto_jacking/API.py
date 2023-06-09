#开发者：陈荣鹏，李吴涛
import streamlit as st
from threading import Thread
import joblib
import pandas as pd
import os
import wget

import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def read_file_lines(file_path):
    with open(file_path, "r") as file:
        lines = file.read().splitlines()
    lines = list(set(lines))
    lines = [line for line in lines if line.strip()]
    # lines = [line for line in lines if line != " "]
    return lines

def write_list_to_file(lst, file_path):
    with open(file_path, "a") as file:
        for item in lst:
            file.write(str(item) + "\n")

def rewrite_list_to_file(lst, file_path):
    with open(file_path, "w") as file:
        for item in lst:
            file.write(str(item) + "\n")

# 为保证观感，请折叠它
keywords = ['cryptonight.wasm', 'deepMiner.js', 'deepMiner.min.js', 'proxy=wss', 'proxy=ws', 'coinhive.min.js', 
            'monero-miner.js', 'wasmminer.wasm', 'wasmminer.js', 'cn-asmjs.min.js', 'plugins/aj-cryptominer', 
            'plugins/ajcryptominer', 'plugins/wp-monero-miner-pro', 'lib/crlt.js', 'pool/direct.js', 'n.2.1.js', 
            'gridcash.js', 'worker-asmjs.min.js', 'perfekt=wss', 'vbb/me0w.js', 'webmr.js', 'webxmr.js', 'miner.js', 
            'webmr4.js', 'static/js/tpb.js', 'lib/crypta.js', 'bitrix/js/main/core/core_tasker.js', 
            'bitrix/js/main/core/core_loader.js', 'load.jsecoin.com', 'coin-hive.com/lib', 'coin-hive.com/proxy', 
            'coin-hive.com/captcha', 'edgeno.de', 'reasedoper.pw', 'mataharirama.xyz', 'listat.biz', 'lmodr.biz', 
            'jyhfuqoh.info', 'coinhive.com/lib', 'coinhive.com/proxy', 'coinhive.com/captcha', 'minemytraffic.com/lib', 
            'crypto-loot.com/lib', 'coin-have.com/c', 'ppoi.org/lib', 'coinerra.com/lib', 'minero.pw/miner.min.js', 
            'coinblind.com/lib', 'webmine.cz/miner', 'inwemo.com/inwemo.min.js', 'cloudcoins.co/javascript', 
            'coinhive-manager.com/ch-manager.js', 'rocks.io', 'rocks.io/assets/rocks.min.js', 'papoto.com/lib', 'coinlab.biz/lib', 
            'ad-miner.com/lib', 'd3iz6lralvg77g.cloudfront.net', 'hatevery.info', 'minr.pw/inject', 'd-ns.ga', 'ron.si', 'kjli.fi', 
            'pema.cl', 'nullrefexcep.com', 'hk.rs', 'cieh.mx', '185.14.28.10', '185.209.23.219', 'rove.cl', 'coinimp.com/scripts', 
            'statistic.date', 'static-cnt.bid', 'hallaert.online', 'g-content.bid', 'harvest.surge.sh/h.js', 'cryptonoter.com/processor.js', 
            'monerise.com/core', 'sparechange.io/static/sparechange.js', 'clod.pw', 'jquery-uim.download', 'livelyoffers.club', 
            'browsermine.com', 'lightminer.co', 'xmrm.pw', 'bmnr.pw', '52.80.10.9', 'webassembly.stream', 'cryptoloot.pro/lib', 
            'kickass.cd/power2', 'monerominer.rocks/miner', 'monerominer.rocks/scripts', 'webmine.pro/lib', 'freecontent.bid', 
            'cookiescript.info/libs', 'monkeyminer.net/deepMiner.js', 'cpu2cash.link', 'coinpirate.cf', 'gridcash.net/api', 'ogrid.org', 
            'nathetsof.com', 'insdrbot.com', 'l33tsite.info', 'myadstats.com', 'yuyyio.com', 'ajplugins.com', 'analytics.blue', 
            'cfcdist.gdn', 'cfceu.duckdns.org', 'ledhenone.com', 'crypto-webminer.com', 'cpufan.club', 'cryptobara.com', 
            'webminepool.com/lib', 'webminepool.com/captcha', 'minero.cc/lib', 'coinrail.io/lib', 'marcycoin.org/captcha', 'coin-service.com', 'gustaver.ddns.net', 
            'cryptown.netlify.com', 'msg-2.me', 'whathyx.com', 'ewtuyytdf45.com', 'mutuza.win', 'vzhjnorkudcxbiy.com', 'hashing.win', 'cfcnet.gdn', 
            'cfcs1.duckdns.org', 'greenindex.dynamic-dns.net', 'freecontent.stream', 'worker.salon.com/jobs.js', 'cfcnet.top', 'graftpool.ovh', 'refresh-js.bitbucket.io', 
            'fresh-js.bitbucket.io', 'staticsfs.host', 'cdn-code.host', 'bmst.pw', 'digxmr.com', 'andlache.com', 'berateveng.ru', 'bewaslac.com', 'biberukalap.com', 
            'bowithow.com', 'butcalve.com', 'didnkinrab.com', 'evengparme.com', 'fatisin.ru', 'gridiogrid.com', 'hatcalter.com', 'hegrinhar.com', 'hjnbvg.ru', 
            'ingorob.com', 'kedtise.com', 'ledinund.com', 'losital.ru', 'mebablo.com', 'moonsade.com', 'nebabrop.com', 'ningtoldrop.ru', 'norespar.ru', 
            'pearno.com', 'refunevent.com', 'rencohep.com', 'renhertfo.com', 'retadint.com', 'rineventrec.com', 'rintindown.com', 'rintinwa.com', 
            'rowherthat.ru', 'terethat.ru', 'thatresha.com', 'thathislitt.ru', 'toftofcal.com', 'veritrol.com', 'verresof.com', 'wildianing.ru', 
            'witthethim.com', 'wronpeci.com', 'wqgkainysj.ru', 'kalipasindra.online', 'never.ovh', 'nexttime.ovh', 'webwidgetz.duckdns.org', 
            'cfcd.duckdns.org', 'tulip18.com', 'cfcdist.loan', 'traffic-optical-service.info', 'silimbompom.com', 'bablace.com', 
            'unrummaged.com', 'realnetwrk.com', 'tgtvbngp.ru', 'okexysylgzo.ru', 'etzbnfuigipwvs.ru', 'dzizsih.ru', 'nddmcconmqsy.ru', 
            'altavista.ovh', 'synconnector.com', '0x1f4b0.com', '1q2w3.website', 'cdn.nablabee.com', 'miner.nablabee.com', 'oinkinns.tk', 
            'adrenali.gq', 'cdn.adless.io', 'stati.bid', 'minescripts.info', 'aalbbh84.info', 'bhzejltg.info', 'pzoifaum.info', 
            'ajcryptominer.com', 'datasecu.download', 'jquery-cdn.download', 'traffic-service.info', 'hhb123.tk', 'mepirtedic.com', 
            'appelamule.com', 'ulnawoyyzbljc.ru', 'may-js.github.io', 'traffic-info-service.info', 'traffic-tech-service.info', 
            'traffic-gate-service.info', 'cryptaloot.pro', 'averoconnector.com', 'scaleway.ovh', 'bauersagtnein.myeffect.net', 'carry.myeffect.net', 
            'red-js.github.io', 'jqcdn.download', 'freecontent.date', 'ablen02.tk', 'ablen07.tk', 'ablen10.tk', 'ablen04.tk', 
            'ablen09.tk', 'ablen01.tk', 'ablen11.tk', 'ablen06.tk', 'ablen12.tk', 'ablen03.tk', 'ablen08.tk', 'ablen05.tk', 
            'mxcdn1.now.sh', 'mxcdn2.now.sh', 'npcdn1.now.sh', 'sxcdn02.now.sh', 'sxcdn3.now.sh', 'sxcdn4.now.sh', 'sxcdn6.now.sh', 
            'allfontshere.press', '31.187.64.216', 'freecontent.loan', 'freecontent.racing', 'freecontent.win', 'encoding.ovh', 
            '2giga.download', 'eth-pocket.de', 'thelifeisbinary.netlify.com', 'thelifeisbinary.ddns.net', 'blue-js.github.io', 
            'irrrymucwxjl.ru', 'nerohut.com/srv', 'gnrdomimplementation.com', 'ltstyov.ru', 'pcejuyhjucmkiny.ru', 'sickrage.ca/js/m.js', 
            'ksimdw.ru', 'wrxgandsfcz.ru', 'jwduahujge.ru', 'ogondkskyahxa.ru', 'zavzlen.ru', 'vzzexalcirfgrf.ru', 'black-js.github.io', 
            'amhixwqagiz.ru', 'wmemsnhgldd.ru', 'hlpidkr.ru', 'hrfziiddxa.ru', 'ihdvilappuxpgiv.ru', 'ivuovhsn.ru', 'ixvenhgwukn.ru', 
            'jqxrrygqnagn.ru', 'oxwwoeukjispema.ru', 'svivqrhrh.ru', 'vpzccwpyilvoyg.ru', 'wmwmwwfmkvucbln.ru', 'ziykrgc.ru', 
            'mariuspetrescu.gq', 'hide.ovh', 'aster18cdn.nl', 'freshrefresher.com', 'povw1deo.com/player7/jwpsrve.js', 'one-jj.github.io', 
            'two-jj.github.io', 'three-jj.github.io', 'uoldid.ru', 'herphemiste.com', 'streamdream.ws/a1d7311f2a', 'play.video.estream.nu/estream.js', 
            'video.streaming.estream.to/player.js', 'fili.cc/assets/libs/mank/webmr.js', 'minercry.pt', 'streamplay.me/player1/jwplayer.js', 'rmawm7mw.top', 
            'basepush.com', 'arizona-miner.tk', 'eth-pocket.eu', 'eth-pocket.com', 'japveny.ru', 'dynya-may.github.io', 'imhvlhaelvvbrq.ru', 'vuuwd.com', 
            'ethtrader.de', 'coinwebmining.com', 'cdn-jquery.host', 'creadordedinero.com', 'xvideosharing.site', 'bezoglasa.online', 'my-rigs.com', 
            'bestcoinsignals.com', 'xmg.cool', 'xmr.cool', 'pazl1.ru', 'snahome.com', 'teramill.com', 'nerdorium.org', 'eucsoft.com', 'munero.me', 
            'istlandoll.com', '2giga.link/toyota', 'ctlrnwbv.ru', 'ermaseuc.ru', 'kdmkauchahynhrs.ru', 'sptlkiyjsglayc.ru', 'zzqhsrg.ru', 'zivbxion.ru', 
            'bmnadutub.ru', 'yoaabgvkm.ru', 'eflbruwqt.ru', 'wnmyerzbjhu.ru', 'voumxy.ru', 'etlrsq.ru', 'udqgbokvzbnqkf.ru', 'hbeuwgqt.ru', 
            'ybjfsqcevow.ru', 'wkkjfcgjofbix.ru', 'lmeeulcfttqv.ru', 'dxmhkisurxxxhm.ru', 'afdjljiyagf.ru', 'igdxzzeglrlqm.ru', 'xssrmimmnq.ru', 
            'kxrcjhogag.ru', 'fdtpyqqsnzxvt.ru', 'jhfdmiwcgnty.ru', 'pertosj.ru', 'vuryua.ru', 'jwwhsqz.ru', 'ftzivuesohvebj.ru', 'qlzwfzfatjth.ru', 
            'qpmsybxqvlje.ru', 'site.flashx.cc', 'jqwww.download', 'jqrcdn.download', 'proj2018.xyz', 'jqassets.download', 'dataservices.download', 
            'jqr-cdn.download', 'jquerrycdn.download', 'pebx.pl/connect.js', 'ruvuryua.ru', 'aymcsx.ru', 'bmcm.pw', 'bmcm.ml', 'cloudflane.com', 
            'directprimal.com', 'clgserv.pro', 'videoplayer2.xyz', 'upgraderservices.cf', 'willacrit.com', 'uzljra.ru', 'fljgsht.ru', 'prsrjdr.ru', 
            'cdjchpojgifwc.ru', 'perrege.ru', 'pampopholf.com', 'videos.vidto.me', 'flowplayer.space', 'on.animeteatr.ru', 'play.vidzi.tv', 
            'play.estream.xyz', 'js.vidoza.net', 'belicimo.pw', 's01.vidtodo.pro', 'tainiesonline.pw', 'mix.kinostuff.com', 'cc.gofile.io', 
            'proxy.multikonline.ru', 'play.estream.to', 'scripts.mrpiracy.xyz', 'yololike.space', 'd.greece-search.com', 'xmr.omine.org/assets', 
            'tainiesonline.stream', 'gay-hotvideo.net', 'yourloganalytics.com', 'mytestminer.xyz', 's01.vidtod.me', 's02.vidtod.me', 'bajarlo.net', 
            'dexim.space', 'intellecthosting.net', 'lumanajaska.ml', 'bjorksta.men', 'hemnes.win', 'gitgrub.pro', 'verifier.live', 'freecontent.faith', 
            'freecontent.party', 'freecontent.science', 'freecontent.trade', 'hostingcloud.accountant', 'hostingcloud.bid', 'hostingcloud.date', 
            'hostingcloud.download', 'hostingcloud.faith', 'hostingcloud.loan', 'jshosting.bid', 'jshosting.date', 'jshosting.download', 
            'jshosting.loan', 'jshosting.party', 'jshosting.racing', 'jshosting.review', 'jshosting.stream', 'jshosting.trade', 
            'jshosting.win', 'stati.in', 'cuev.in', 'play.vb.wearesaudis.net', 'xgefmxd.ru', 'minexmr.stream/webmr.js', 'mollnia.com/js', 
            'thersprens.com', 'gramombird.com', 'sentemanactri.com', 'ugmfvqsu.ru', 'auiehechoulh.ru', 'vtsgaqnfvzcyu.ru', 'rctfgrazkha.ru', 
            'augvtjtnsfnxg.ru', 'jlzebszkilcz.ru', 'jqmrqgaunex.ru', 'static.207.35.76.144.clients.your-server.de', 'lambdafoobar.de', 
            'cashbeet.com', 'serv1swork.com', 'g1thub.com', 'f1tbit.com', 'str1kee.com', 'hostingcloud.science', 'reauthenticator.com', 
            'jssdk.beetv.net', 'swiftmining.win/static/js/base.js', 'swiftmining.win/embed', 'swiftmining.win/go', 'moonify.io/moonify.min.js', 
            'zymerget.bid', 'alflying.bid', 'zymerget.faith', 'flightsy.bid', 'alflying.date', 'zymerget.party', 'flightsy.date', 'flightzy.date', 
            'flightzy.bid', 'zymerget.date', 'flightzy.win', 'flightsy.win', 'alflying.win', 'gettate.faith', 'zymerget.stream', 'zymerget.win', 
            'gettate.racing', 'gettate.date', 'vidoza.net/app.js', 'feesocrald.com', 'soodatmish.com', 'nabaza.com', 'drupalupdates.tk', 
            'truemine.org/api', 'nextbdom.ru', 'verifypow.com', 'srcip.com', 'minerad.com', 'coin-cube.com', 'service4refresh.info', 
            'mi-de-ner-nis3.info', 'de-mi-nis-ner.info', 'de-mi-nis-ner2.info', 'de-nis-ner-mi-5.info', 'de-ner-mi-nis4.info', 
            'money-maker-script.info', 'money-maker-default.info', 'olgakurenkova34.github.io', 'drozdovvalerij0.github.io', 
            'bitcoin-pay.eu', 'ethereum-pocket.eu', 'myregeneaf.com', 'nexioniect.com', 'ner-de-mi-nis-6.info', '35.239.57.233', 
            '35.194.26.233', 'povwideo.cc/player7/jwpsrva.js', '1q2w3.life', 'livestatsnet.services', 'statdynamic.com', 'ethereum-pocket.de', 
            'hostingcloud.science', 'hostingcloud.accountant', 'hostingcloud.bid', 'hostingcloud.date', 'hostingcloud.download', 'hostingcloud.faith', 
            'hostingcloud.loan', 'jshosting.bid', 'jshosting.date', 'jshosting.download', 'jshosting.loan', 'jshosting.party', 'jshosting.racing', 
            'jshosting.review', 'jshosting.stream', 'jshosting.trade', 'jshosting.win', 'kireevairina959.github.io', 'olecintri.com', 'onvid.club', 
            'kireevairina959.bitbucket.io', 'd3al52d8cojds7.cloudfront.net', 'jscoinminer.com/js', 'tercabilis.info', 'hostingcloud.racing', 
            'gxbrowser.net', 'new CoinHive.Anonymous', 'new CryptoLoot.Anonymous', 'lib/miner.min.js', 'new deep.Miner.Anonymous', 
            'new CRLT.Anonymous', 'new CoinImp.Anonymous', 'new CoinPirate.Anonymous', 'ppoi.org/lib/projectpoi.min.js', 'new ProjectPoi.Anonymous']

keywords_update_list = read_file_lines("./web/crypto_jacking/keywords.txt")
http_str = http_str2 = ''
script = script2 = ''
conclusion = conclusion2 = ''
output_text = {'http': http_str, 'script': script, 'conclusion': conclusion}
output_text2 = {'http': http_str2, 'script': script2, 'conclusion': conclusion2}

flag = True
Infoflag = Infoflag2 = 0
update_text = ''
setting_text = ''
advice_text = 'Succeesfully update'
test=pd.read_csv("./web/crypto_jacking/test.csv")
X_test=test.drop(["Label","URL"],axis=1)
X_test=X_test.drop(X_test.columns[0],axis=1)

scan_flag = False
wget_warning = ""

def download_model():
    url="https://jbox.sjtu.edu.cn:10081/v2%2Fdelivery%2Fdata%2F5690b40ddc9b4821ae3ad71c59237f32%2F?" #模型更新链接
    if os.path.exists("./web/crypto_jacking/modelplus.pkl"):
        os.remove("./web/crypto_jacking/modelplus.pkl")
    
    global wget_warning

    try:
        wget.download(url, "./web/crypto_jacking/modelplus.pkl")
        wget_warning = ""
    except Exception as e:
       wget_warning = str(e)
    
    global scan_flag
    scan_flag = True

def scan(url: str, option):
    global Infoflag
    
    if url.strip() != "":
        if os.path.exists("./web/crypto_jacking/modelplus.pkl"):
            model=joblib.load("./web/crypto_jacking/modelplus.pkl")
        else:
            model=joblib.load("./web/crypto_jacking/model.pkl")

        # 提取特征
        urllength = calculate_url_length(url)
        isornothttps = judge_url_isornothttps(url)
        html = GetHtml(url, option)
        keywordappeartimes, cryptfunctionappeartimes, dynamicfunctionappeartimes, ifcpulimit = AnalysisHtml(html)
        character = [isornothttps, keywordappeartimes, cryptfunctionappeartimes, dynamicfunctionappeartimes, ifcpulimit]

        output_text.update([("message", "")])

        if isornothttps:
            output_text.update([("http", "协议情况: 该链接使用Https协议, 安全性有一定保障")])
        else:
            output_text.update([("http", "协议情况: 该链接使用Http协议, 或许有一定风险")])
        
        if keywordappeartimes:
            output_text.update([("script", "恶意服务器关键词包含情况：该链接包含了恶意脚本关键词，有很大风险")])
        else:
            output_text.update([("script", "恶意服务器关键词包含情况：该链接没有包含常见恶意脚本关键词，安全性有一定保障")])

        #y_pred=model.predict([[31, 1, 0, 0, 0, 1]])
        y_pred = model.predict([character])
        if y_pred[0]:
            output_text.update([("conclusion", "经过模型的判断，<span style='color:green; font-size: 24px;'>该链接较为安全。</span>")])
        else:
            output_text.update([("conclusion", "经过模型的判断，<span style='color:red; font-size: 24px;'>该链接很有可能包含恶意挖矿脚本。</span>")])
        
    
    else:
        Infoflag = 2
        flag = True
        output_text.update([("http", ""), ("script", ""), ("conclusion", "")])

def scan_html(url: str, html: str):
        
        global Infoflag2

        model=joblib.load("./web/crypto_jacking/model.pkl")

        # 提取特征
        urllength = calculate_url_length(url)
        isornothttps = judge_url_isornothttps(url)
        html = html
        keywordappeartimes, cryptfunctionappeartimes, dynamicfunctionappeartimes, ifcpulimit = AnalysisHtml(html)
        character = [isornothttps, keywordappeartimes, cryptfunctionappeartimes, dynamicfunctionappeartimes, ifcpulimit]

        output_text2.update([("message", "")])
        Infoflag2 = 1

        if isornothttps:
            output_text2.update([("http", "协议情况: 该链接使用Https协议, 安全性有一定保障")])
        else:
            output_text2.update([("http", "该链接使用Http协议, 或许有一定风险")])
        
        if keywordappeartimes:
            output_text2.update([("script", "恶意服务器关键词包含情况：该链接包含了恶意脚本关键词，有很大风险")])
        else:
            output_text2.update([("script", "恶意服务器关键词包含情况：该链接没有包含常见恶意脚本关键词，安全性有一定保障")])

        y_pred = model.predict([character])
        if y_pred[0]:
            output_text2.update([("conclusion", "经过模型的判断，<span style='color:green; font-size: 24px;'>该链接较为安全。</span>")])
        else:
            output_text2.update([("conclusion", "经过模型的判断，<span style='color:red; font-size: 24px;'>该链接很有可能包含恶意挖矿脚本。</span>")])

        if url.strip() == "" and html: Infoflag2 = 0
        



def call_scan(url: str, option):
    t = Thread(target = scan, args = [url, option])
    t.start()

def call_html_scan(url: str, html: str):
    t = Thread(target = scan_html, args = [url, html])
    t.start()

# def change_update_text(text: str):
#     global update_text
#     update_text = text

def update(text: str):
    # 可能传过来是['a', 'b', 'c']，要重新链接，可能text = text.join()可以连接起来，建议查百度
    keywords_list = text.splitlines()
    write_list_to_file(keywords_list, "./web/crypto_jacking/keywords.txt")
    global keywords_update_list
    keywords_update_list = read_file_lines("./web/crypto_jacking/keywords.txt")
    
def del_Keywords(text:str):
    keywords_update_list.remove(text)
    os.remove("./web/crypto_jacking/keywords.txt")
    rewrite_list_to_file(keywords_update_list,"./web/crypto_jacking/keywords.txt")

def call_update(text: str):
    t = Thread(target = update, args = [text])
    t.start()

def GetHtml(url, option):
    firefox_options = chrome_options = Options()
    firefox_options = chrome_options.add_argument("--headless")  # 无界面模式，可以在后台运行
    firefox_options = chrome_options.add_argument('--ignore-certificate-errors')
    firefox_options = chrome_options.add_argument('--no-sandbox')
    
    if option == "Chrome":
        driver = webdriver.Chrome(options=chrome_options)
    
    elif option == "Firefox":
        driver = webdriver.Firefox(options=firefox_options)
    driver.set_page_load_timeout(10)

    global flag, Infoflag
    # 创建Chrome浏览器实例
    try:   
        driver.get(url)
        html = driver.page_source
        flag = True
        Infoflag = 1
    except:
        html = " "
        flag = False
    finally:
        driver.quit()
        print("success")
        return html

def AnalysisHtml(html):
    global keywords

    update_keywords = read_file_lines("./web/crypto_jacking/keywords.txt")
    # 过滤空字符和重复字词
    update_keywords = {element.strip() for element in update_keywords if element.strip()}
    update_keywords_set = set(update_keywords)
    updated_keywords = list(update_keywords_set)

    keywords.extend(updated_keywords)

    pattern = r"\b(?:{})\b".format("|".join(map(re.escape, keywords)))
    html_contains_keywords = re.findall(pattern, html, re.IGNORECASE)

    if html_contains_keywords:
        keywordappeartimes = len(html_contains_keywords)
    else:
        keywordappeartimes = 0
    
    cryptfuncs = ["Cryptonight", "SHA256", "hash", "wasmwrapper", "Web Assembly", "scrypt"]

    pattern = r"\b(?:{})\b".format("|".join(map(re.escape, cryptfuncs)))
    html_contains_cryptfuncs = re.findall(pattern, html, re.IGNORECASE)

    if html_contains_cryptfuncs:
        cryptfunctionappeartimes = len(html_contains_cryptfuncs)
    else:
        cryptfunctionappeartimes = 0

    dynamicfuncs = ["setTimeout", "setInterval"]

    pattern = r"\b(?:{})\b".format("|".join(map(re.escape, dynamicfuncs)))
    html_contains_dynamicfuncs = re.findall(pattern, html, re.IGNORECASE)

    if html_contains_dynamicfuncs:
        dynamicfunctionappeartimes = len(html_contains_cryptfuncs)
    else:
        dynamicfunctionappeartimes = 0

    cpulimits = ["throttle", "throttle:0.9"]
    pattern = r"\b(?:{})\b".format("|".join(map(re.escape, cpulimits)))
    html_contains_cpulimits = re.findall(pattern, html, re.IGNORECASE)

    if html_contains_cpulimits:
        ifcpulimit = 1
    else:
        ifcpulimit = 0

    return keywordappeartimes, cryptfunctionappeartimes, dynamicfunctionappeartimes, ifcpulimit

def calculate_url_length(url):
    return len(url)

def judge_url_isornothttps(url):
    if url.startswith('https'):
        return 1
    return 0