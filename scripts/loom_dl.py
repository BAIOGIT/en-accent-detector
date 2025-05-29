import requests
import os
from pathlib import Path
from urllib.parse import urlparse

def fetch_loom_download_url(video_id):
    try:
        url = f"https://www.loom.com/api/campaigns/sessions/{video_id}/transcoded-url"
        headers = {
            "content-type": "application/json; charset=utf-8",
            # "content-length": "712",
            # "date": "Thu, 29 May 2025 11:47:56 GMT",
            # "vary": "Accept-Encoding",
            # "cache-control": "private, no-cache, no-store, must-revalidate",
            # "expires": "-1",
            # "pragma": "no-cache",
            # "referrer-policy": "strict-origin-when-cross-origin",
            # "x-content-type-options": "nosniff",
            # "x-frame-options": "DENY",
            # "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
            # "content-security-policy": "default-src 'self' blob: ; script-src 'nonce-lH2yTpQwOOICihlwHA6OD0iaXILrx0I5RggKQL5gG9SPXbrp' 'self' 'unsafe-eval' 'unsafe-inline' 'strict-dynamic' blob: https: ; style-src 'unsafe-inline' https://cdn.loom.com https://releases.transloadit.com/uppy/ https://accounts.google.com/gsi/style https://ds-cdn.prod-east.frontend.public.atl-paas.net/assets/; img-src 'self' blob: data: chrome-extension: https:; font-src 'self' data: chrome-extension: https://cdn.loom.com https://fonts.gstatic.com https://use.typekit.net https://ds-cdn.prod-east.frontend.public.atl-paas.net/assets/ https://js.intercomcdn.com https://fonts.intercomcdn.com https://jcs-chat-widget.atlassian.com/assets/; base-uri 'self'; connect-src 'self' data: https://bat.bing.com https://*.clarity.ms https://*.mutinyhq.com https://*.mutinyhq.io https://*.mutinycdn.com https://*.google.com https://accounts.google.com/gsi/ https://*.analytics.google.com https://*.google-analytics.com https://*.googletagmanager.com https://*.g.doubleclick.net https://connect.facebook.net https://px.ads.linkedin.com https://pixel-config.reddit.com https://q.quora.com https://analytics.tiktok.com/ https://www.redditstatic.com/ads/ https://api.segment.io https://cdn.segment.com https://intercom.help https://api-iam.intercom.io https://api-iam.eu.intercom.io https://api-iam.au.intercom.io https://api.hubapi.com https://cta-service-cms2.hubspot.com https://js.hs-banner.com https://js.hubspot.com/web-interactives-embed.js https://browser-http-intake.logs.datadoghq.com/ https://logs.browser-intake-datadoghq.com/api/ https://rum.browser-intake-datadoghq.com/api/ https://m.stripe.com https://o398470.ingest.sentry.io https://loom-media-production.s3.us-west-2.amazonaws.com/uploads/ https://loom-media-production.s3.us-west-2.amazonaws.com/sessions/ https://s3.us-west-2.amazonaws.com/loom-media-production/sessions/ https://s3.us-west-2.amazonaws.com/loom-media-production/images/ https://s3.us-west-2.amazonaws.com/loom-screenshots-production/images/ https://loom-prd-usw2-media.s3.us-west-2.amazonaws.com/uploads/ https://s3.us-west-2.amazonaws.com/loom-prd-usw2-media/sessions/ https://s3.us-west-2.amazonaws.com/loom-prd-usw2-media/images/ https://s3.us-west-2.amazonaws.com/loom-prd-usw2-media/images/ https://*.loom.com wss://www.loom.com https://*.atlassian.com https://cdn.cookielaw.org https://geolocation.onetrust.com https://privacyportal.onetrust.com https://cookie-cdn.cookiepro.com https://*.atl-paas.net https://calendly.com; media-src 'self' blob:  data: https://*.loom.com/ https://cdn.sanity.io  https://js.intercomcdn.com https://downloads.intercomcdn.com https://downloads.intercomcdn.eu https://downloads.au.intercomcdn.com; object-src 'none'; frame-src 'self' https://js.stripe.com https://www.loom.com https://accounts.google.com/gsi/ https://www.google.com/ https://*.doubleclick.net https://calendly.com https://useloom.atlassian.net; report-uri https://browser-intake-datadoghq.com/api/v2/logs?dd-api-key=pub18c86b072f3b6cefdae2b56c8b60db94&dd-evp-origin=content-security-policy&ddsource=csp-report&ddtags=service%3Acsp%2Cenv%3Aproduction",
            # "etag": 'W/"2c8-S7Yav+PXh0Du9V0/L90gz1GEoI8"',
            # "x-cache": "Miss from cloudfront",
            # "via": "1.1 9a3c643f228eb943137621235dabf790.cloudfront.net (CloudFront)",
            # "x-amz-cf-pop": "MXP64-P1",
            # "alt-svc": 'h3=":443"; ma=86400',
            # "x-amz-cf-id": "JATb7r7gccAeW8HqzX3UUCSBNvHU5fQUN6rGyUD-57HTOvmNEIVvUg==",
            # "x-cdn": "cloudfront",
            # "vary": "Origin",
            # "server-timing": 'cdn-upstream-layer;desc="EDGE",cdn-upstream-dns;dur=0,cdn-upstream-connect;dur=0,cdn-upstream-fbl;dur=260,cdn-cache-miss,cdn-pop;desc="MXP64-P1",cdn-rid;desc="JATb7r7gccAeW8HqzX3UUCSBNvHU5fQUN6rGyUD-57HTOvmNEIVvUg==",cdn-downstream-fbl;dur=264'
        }
    
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {'success': True, 'message': 'Fetched data', 'data': data.get('url')}
    except Exception as e:
        return {'success': False, 'message': 'There are some issues while fetching loom download URL.', 'data': None}

def download_loom_video(url, filename):
    try:
        dir_path = Path('downloads')
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / filename

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return {'success': True, 'message': 'Video has been downloaded successfully.'}
    except Exception as e:
        return {'success': False, 'message': 'There are some issues while downloading video.'}

def is_loom_video_url(url):
    loom_domain = 'www.loom.com'
    trimmed_url = url.strip()
    return trimmed_url.startswith('https://') and loom_domain in trimmed_url

def get_id(video_url):
    return video_url.rstrip('/').split('/')[-1].split('?')[0]

def main(video_url):
    video_id = get_id(video_url)
    url_response = fetch_loom_download_url(video_id)
    if url_response['success']:
        filename = f"{video_id}.mp4"
        response = download_loom_video(url_response['data'], filename)
        return response
    return url_response

# Example usage:
if __name__ == "__main__":
    url = "https://www.loom.com/share/9edb010ba5344833b48ef281380cedaa"
    result = main(url)
    print(result)
