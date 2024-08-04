
import requests
from selectolax.parser import HTMLParser
import pandas as pd
import os
import json
import re
from seleniumbase import SB
from rich import print
import time


root_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(root_path)

csv_file = 'g2_badge.csv'
last_index = 0

badge_css = 'div[class="status-badge__label"]'
read_path = os.path.join(root_path,'g2 only product.csv')
readcsv = pd.read_csv(read_path)

productsLinks = readcsv['Product Link'].to_list()
         
with SB(uc=True) as sb:
    for index, productLink in enumerate(productsLinks[last_index:], start=last_index + 2):
        print(f'>= {index} - {productLink}')
        
        try:
            sb.set_window_size(600, 800)
            sb.uc_open_with_reconnect(productLink, 5)
            sb.sleep(1)
            sb.uc_gui_click_cf()
            sb.sleep(2)
            # sb.wait_for_element('body', timeout=10)

            try:
                badge = sb.get_text(badge_css)
            except Exception as e:
                # print(f">= Error extracting badge: {e}")
                badge = ''

            company_data = {
                'Product Link': productLink,
                'Badge': badge
            }
        
            df = pd.DataFrame([company_data])
            df.to_csv(csv_file, mode='a', index=False, header=not os.path.exists(csv_file))

        except Exception as e:
            print(f">= Error processing link {index} - {productLink}: {e}")
            break

