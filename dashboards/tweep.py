{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "2797abbc-0c49-470c-814c-e878fa9b65e2",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import the required libraries and dependencies\n",
    "import pytest\n",
    "import pandas as pd\n",
    "import os\n",
    "from dotenv import load_dotenv\n",
    "import requests\n",
    "import json\n",
    "import urllib.request\n",
    "import tweepy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "f244f297-bb9e-4cfb-9b49-01130429894f",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Python-dotenv could not parse statement starting at line 1\n"
     ]
    }
   ],
   "source": [
    "# Load .env environment variables\n",
    "load_dotenv()\n",
    "\n",
    "tweepy_consumer_key = os.getenv(\"TWITTER_CONSUMER_KEY\")\n",
    "tweepy_consumer_secret = os.getenv(\"TWITTER_CONSUMER_SECRET\")\n",
    "tweepy_access_token = os.getenv(\"TWITTER_ACCESS_TOKEN\")\n",
    "tweepy_access_token_secret = os.getenv(\"TWITTER_ACCESS_TOKEN_SECRET\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "cf363e07-cf98-44de-84ae-148db567b7ec",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "RT @foodmasku: Delectables are over 90% minted! I love the 1/1 backgrounds that have been revealed!\n",
      "\n",
      "@tonsoccr @taniadelrio @JimenaBuenaVid…\n",
      "RT @HollanderAdam: Successfully minted 🔥\n",
      "\n",
      "All those years of crafting in MMOs paying off 🎮\n",
      "\n",
      "Looking forward to creating more of these 🚀 htt…\n",
      "RT @MechaChaoticNFT: Some of the damage from @EthanSBrewerton's raid streams from today.  @BoredApeYC @MetaHero_ @the_vogu @ToyBoogers \n",
      "\n",
      "Wh…\n",
      "@MechaChaoticNFT @EthanSBrewerton @BoredApeYC @MetaHero_ @the_vogu @mattborchert @NsightNFT @glypsie So awesome!!!… https://t.co/H9L0wSTk2p\n",
      "Después de casi 24 horas de haber lanzado el #DespliegueNacional, podemos anunciar que hemos contenido el alza de v… https://t.co/lOC1dN396Y\n",
      "So ladies and gentlemen...\n",
      "\n",
      "- Follow me and follow @terra_bots_io \n",
      "- Join their discord: https://t.co/gR9ZH35icn\n",
      "-… https://t.co/iZxe0jNPwA\n",
      "My Toy Boogers NFTs are all 100% hand drawn and hand made. Started with pen on paper, then photographed, vectorized… https://t.co/tZoK8FmQvF\n",
      "RT @DreadBong0: Going to be super interesting to see just how hard $AZERO runs when it launches this month..\n",
      "\n",
      "The hype is real 🔥\n",
      "35k baby 🤍🙏😌\n",
      "RT @sparks_jpg: This man @jamsjetson out of the kindness of heart just sent me a @GEVOLsNFT No questions. Just pure kindness. I have only b…\n",
      "RT @0x_emperor: @DegenSpartan you arent airdropped alfa, you are airdropped personal responsibility\n",
      "@godeLives The chart.. it started\n",
      "\n",
      "$100 programmed now\n",
      "@beaniemaxi this is the kinda genius that I know you're capable of\n",
      "RT @MorganStoneee: Busy day both in IRL + project planning, so didn't have time earlier, but.....\n",
      "\n",
      "🚨WHITELIST GAMES DAY 3 LET'S GET IT!!!!!…\n",
      "RT @Reflog_18: @NFL @obj @RamsNFL Mint this https://t.co/orp8hzVKQH\n",
      "Booked ✈️ to SFO Dec. 10 &amp; 11th\n",
      "I love y’all 💜\n",
      "RT @TitanXBT: Nothing can make me sell my @Portals_Art i am diamond fisting tf out of life changing money with an elite crew fuck off telli…\n",
      "#NFT #NFTs #nftart #NFTcollectibles #NFTdrop #NFTshill #NFTartwork #NFTshilling #nftcollector #wagmi #Ethereum #ETH… https://t.co/NTH3FYuaba\n",
      "🚨  91,709,779 #TRX (10,093,983 USD) transferred from #Binance to unknown wallet\n",
      "\n",
      "https://t.co/pldfvPbpgW\n"
     ]
    }
   ],
   "source": [
    "tweepy_auth = tweepy.OAuthHandler(tweepy_consumer_key, tweepy_consumer_secret)\n",
    "tweepy_auth.set_access_token(tweepy_access_token, tweepy_access_token_secret)\n",
    "\n",
    "api = tweepy.API(tweepy_auth)\n",
    "\n",
    "public_tweets = api.home_timeline()\n",
    "for tweet in public_tweets:\n",
    "    print(tweet.text)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b223edd6-52bf-4541-9bd3-afcef2702e71",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "da87ffb3-286f-4352-b59b-6dff2523656a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.10"
  },
  "widgets": {
   "application/vnd.jupyter.widget-state+json": {
    "state": {},
    "version_major": 2,
    "version_minor": 0
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
