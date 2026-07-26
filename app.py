#code by @raigenffofc 
#code by @raigenffofc 
import binascii
import logging
from datetime import datetime

import requests
from flask import Flask, jsonify, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from GetWishListItems_pb2 import CSGetWishListItemsRes
import uid_generator_pb2
from token_raigen import ensure_xxx_sync

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DEFAULT_KEY = "Yg&tc%DEuh6%Zc^8"
DEFAULT_IV = "6oyZDr22E3ychjM%"

API_ENDPOINTS = {
    "IND": "https://client.ind.freefiremobile.com/GetWishListItems",
    "BR": "https://client.us.freefiremobile.com/GetWishListItems",
    "US": "https://client.us.freefiremobile.com/GetWishListItems",
    "SAC": "https://client.us.freefiremobile.com/GetWishListItems",
    "NA": "https://client.us.freefiremobile.com/GetWishListItems",
    "default": "https://clientbp.ggblueshark.com/GetWishListItems"
}

def convert_timestamp(release_time):
    return datetime.utcfromtimestamp(release_time).strftime('%Y-%m-%d %H:%M:%S')

def encrypt_aes(hex_data, key, iv):
    key_bytes = key.encode()[:16]
    iv_bytes = iv.encode()[:16]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    padded_data = pad(bytes.fromhex(hex_data), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return binascii.hexlify(encrypted_data).decode()

def fetch_wishlist_from_api(idd, region):
    token = ensure_xxx_sync(region)
    if not token:
        raise ValueError(f"Failed to retrieve auth token for region: {region}")    
        
    endpoint = API_ENDPOINTS.get(region, API_ENDPOINTS["default"])    
    
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
        'Connection': 'Keep-Alive',
        'Expect': '100-continue',
        'Authorization': f'Bearer {token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB52',
        'Content-Type': 'application/x-www-form-urlencoded',
    }    
    
    try:
        data_bytes = bytes.fromhex(idd)
        response = requests.post(
            endpoint,
            headers=headers,
            data=data_bytes,
            timeout=10
        )
        response.raise_for_status()
        return response.content.hex()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise

@app.route('/wish', methods=['GET'])
def get_player_info():
    try:
        uid = request.args.get('uid')
        region = request.args.get('region', 'default').upper()
        custom_key = request.args.get('key', DEFAULT_KEY)
        custom_iv = request.args.get('iv', DEFAULT_IV)
        
        if not uid:
            return jsonify({"error": "UID parameter is required"}), 400
            
        message = uid_generator_pb2.uid_generator()
        message.saturn_ = int(uid)
        message.garena = 1
        protobuf_data = message.SerializeToString()
        
        hex_data = binascii.hexlify(protobuf_data).decode()
        encrypted_hex = encrypt_aes(hex_data, custom_key, custom_iv)
        
        api_response_hex = fetch_wishlist_from_api(encrypted_hex, region)         
        if not api_response_hex:
            return jsonify({"error": "Empty response received"}), 400
            
        api_response_bytes = bytes.fromhex(api_response_hex)
        decoded_response = CSGetWishListItemsRes()
        decoded_response.ParseFromString(api_response_bytes)    
        
        wishlist = [
            {
                "item_id": item.item_id, 
                "release_time": convert_timestamp(item.release_time)
            }
            for item in decoded_response.items
        ]            
        return jsonify({"uid": uid, "region": region, "wishlist": wishlist})
        
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logging.error(f"Error processing: {e}")
        return jsonify({"error": f"Failure: {str(e)}"}), 500

@app.route('/favicon.ico')
def favicon():
    return '', 404

if __name__ == "__main__":
    logging.info("Starting Server...")
    ensure_xxx_sync("default")
    app.run(host="0.0.0.0", port=5552)
#code by @raigenffofc 
#code by @raigenffofc 
#modified by raigen rohan