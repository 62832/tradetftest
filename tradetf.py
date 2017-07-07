import json
import requests
import time

QUALITIES = {"uncraft"    : - 1,
             "genuine"    :   1,
             "vintage"    :   3,
             "unique"     :   6,
             "strange"    :  11,
             "haunted"    :  13} # all qualities currently tracked by Trade.TF

CURRENCIES = {"r": " refined",
              "k": " keys"   ,
              "b": " buds"   }

def get_item_defindex(item_name):
    for items in schema:
        if items["name"].lower() == item_name.lower():
            return items["defindex"]
    else:
        print("Invalid item.")
        return None

def get_tradetf_price(item, quality):
    item_data = spreadsheet[str(item)][str(quality)]["regular"]
    price = item_data["hi"]
    unit  = CURRENCIES[item_data["unit"]]
    return str(price) + unit

def get_input(dialog, valid_inputs, error_message):
    while True:
        answer = input(dialog)
        if answer.lower() in valid_inputs:
            return answer
        else:
            print(error_message)

def main():
    while True:
        item_name = str(input("Enter item name: "))
        item_ = get_item_defindex(item_name)
        if item_:
            break
    
    quality = get_input(
        "Enter item quality: ", QUALITIES,
        "Quality not tracked by Trade.tf."
    )
    quality_ = QUALITIES[quality.lower()]
    
    try:
        print("\n {} {} price: {}".format(quality, item_name,
                                          get_tradetf_price(item_, quality_)))
    except KeyError:
        print("Item not currently tracked by Trade.tf.")

if __name__ == "__main__":
    
    with open('keys.json', 'r') as f:
        keys = json.load(f)
        try:
            schema = requests.get('http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key=' + keys['steam']).json()['result']['items']
            spreadsheet = requests.get('http://www.trade.tf/api/spreadsheet.json?key=' + keys['tradetf']).json()['items']
            main()
        except json.decoder.JSONDecodeError:
            print("INVALID API KEYS DETECTED.")
    
    print("Shutting down...")
    time.sleep(3)
