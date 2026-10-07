"""Mightypreneur advanced CSV: blog pins for Gifts for Mom + Teacher Gifts (3 each). Times Eastern; CSV read as Pacific (-3h)."""
import csv, sys, datetime as dt
sys.path.insert(0, 'tools')
from make_pin_csv import ROW1, ROW2
IMG = "https://raw.githubusercontent.com/jessicajsantiago/lookslikeluxe/main/pins"
SITE = "lookslikeluxe.netlify.app/blog"
D = " As an Amazon Associate I earn from qualifying purchases."
PINS_DECOR = [
 ("amazon-christmas-decor", "amazon-christmas-decor-v1-grid.png", dt.datetime(2026,10,11,15), "Amazon Christmas Decor That Looks Designer: 8 Finds",
  "Amazon Christmas decor that looks designer: a pre-lit tree, nutcrackers, gold mercury glass ornaments, velvet bows and more. Eight festive finds with great reviews. Tap for the full list." + D + " #christmasdecor #amazonchristmas #holidaydecor"),
 ("amazon-christmas-decor", "amazon-christmas-decor-v2-hero.png", dt.datetime(2026,10,15,15), "Burgundy and Gold Christmas Decor from Amazon",
  "Burgundy and gold Christmas decor from Amazon that looks way more expensive than it is. Velvet bows, nutcrackers, gold ornaments and a glowing village. See all 8 picks." + D + " #burgundychristmas #christmasdecorideas"),
 ("amazon-christmas-decor", "amazon-christmas-decor-v3-list.png", dt.datetime(2026,10,19,15), "Best Amazon Christmas Decor Finds (Designer Look)",
  "The best Amazon Christmas decor finds for a designer look: tree, bows, candles and mantel pieces. Eight ideas with real reviews. Tap to browse the list." + D + " #amazonfinds #christmasmantel #holidayhome"),
]
PINS = [
 ("gifts-for-mom", "gifts-for-mom-v1-grid.png", dt.datetime(2026,10,8,15), "Christmas Gifts for Mom: 8 Ideas She'll Actually Love",
  "Christmas gifts for mom that go way beyond a candle: a salon-style hair styler, a digital photo frame, a smart herb garden, a Ninja Creami and more. Thoughtful Amazon gift ideas with great reviews. Tap for all 8." + D + " #giftsformom #christmasgiftideas"),
 ("teacher-gifts", "teacher-gifts-v1-grid.png", dt.datetime(2026,10,9,15), "Teacher Gifts That Aren't Mugs: 8 Ideas She'll Actually Use",
  "Teacher gifts that aren't mugs: a YETI tumbler, UGG slippers, a Kindle, a spa basket and more. Christmas teacher gift ideas from Amazon that are useful and pretty. Tap for all 8." + D + " #teachergifts #christmasgiftideas"),
 ("gifts-for-mom", "gifts-for-mom-v2-hero.png", dt.datetime(2026,10,13,15), "Gift Ideas for Mom Who Says She Wants Nothing",
  "She said don't get me anything. She lied. Eight Christmas gift ideas for mom, from a Ninja Creami to a KitchenAid mixer, all with great Amazon reviews. See the full list." + D + " #giftideasformom #momgifts"),
 ("teacher-gifts", "teacher-gifts-v2-hero.png", dt.datetime(2026,10,14,15), "Best Christmas Gifts for Teachers (Not a Mug)",
  "The best Christmas gifts for teachers: practical, pretty and not another mug. A Kindle, cozy slippers, a work tote and more. See all 8 picks." + D + " #teachergiftideas #christmasgifts"),
 ("gifts-for-mom", "gifts-for-mom-v3-list.png", dt.datetime(2026,10,17,15), "Best Amazon Gifts for Mom This Christmas",
  "The best Amazon gifts for mom this Christmas: eight picks that look thoughtful because they are. Kitchen upgrades, cozy gifts and sentimental ones. Tap to browse the list." + D + " #amazongifts #christmasgiftsformom"),
 ("teacher-gifts", "teacher-gifts-v3-list.png", dt.datetime(2026,10,18,15), "Unique Teacher Christmas Gifts She'll Actually Use",
  "Unique teacher Christmas gifts from Amazon: a tumbler, a spa basket, hand warmers and a candle warmer lamp. Eight ideas that say thank you. Tap to browse the list." + D + " #teacherchristmasgifts #giftsforteachers"),
]
rows=[ROW1,ROW2]
for slug,img,et,title,desc in (PINS_DECOR if (len(sys.argv)>2 and sys.argv[2]=="decor") else PINS):
    pt=et-dt.timedelta(hours=3); r=[""]*40
    r[0]=pt.strftime("%Y-%m-%d %H:%M:%S"); r[1]=desc; r[3]=f"{IMG}/{img}"; r[7]="false"; r[8]="false"; r[38]=title; r[39]=f"{SITE}/{slug}.html"
    rows.append(r); print(et.strftime("%a %b %d %I:%M %p ET"),slug,img,len(title),len(desc))
csv.writer(open(sys.argv[1] if len(sys.argv)>1 else "pins-mom-teacher.csv","w",newline="",encoding="utf-8")).writerows(rows)
