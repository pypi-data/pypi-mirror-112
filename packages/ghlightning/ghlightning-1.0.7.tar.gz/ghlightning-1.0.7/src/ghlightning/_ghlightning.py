#!/usr/bin/env python3
# Will Being Coded By: Nader.
"""
A Python module wh_ose function is to extract the information of github users
download their photos, _get a lot of information about the country of any user
on github, know a number of his followers, download his followers pictures
and many, many advantages that you can try!
########################
Was Developed By: Nader.
########################
"""

import os as _os
from urllib.request import urlretrieve as _urlretrieve
import pathlib as _pathlib
import countryinfo as _countryinfo
import requests.exceptions as _requestsexceptions
from requests import get as _get
from bs4 import BeautifulSoup as _BeautifulSoup
from math import ceil as _ceil
import user_agent
from .errors import *

""" ERRORS EXCEPTIONS """


class Github:
    """ Pass a Github username to the object of this class to begin collect information!"""

    current_path = _os.getcwd()  # class attribute.

    def __init__(self, username):
        self.username = username
        self.url = f"https://github.com/{self.username}"
        self.__headersDic = {
            "Authorization": "token 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"
        }

        if not _get(f"https://github.com/{self.username}"):
            raise UsernameNotFound(f"{self.username} is NOT existed on Github.")

        self.__resp = _get(f"https://api.github.com/users/{self.username}",
                           headers={"User-Agent": user_agent.generate_user_agent()}).json()

        try:
            self.userId = self.__resp["id"]
        except:
            self.userId = None

        self.__headers = {"Host": "github.com",
                          "User-Agent": user_agent.generate_user_agent(),
                          "Accept-Language": "en-US,en;q=0.5",
                          "Accept-Encoding": "gzip, deflate, br",
                          "Referer": "https://github.com",
                          "Connection": "keep-alive",
                          "Cookie": "user_session=kwO7LcPSqCVUguEf7xonR6ycKmuqm8XvI0qVco0FjE1ZKY1w;"}

        try:
            countryName = str(self.__resp["location"]).split(",")[1].strip()
            if len(countryName.split(",")) == 2:
                self.countryName = countryName.split(",")[1]
            elif len(countryName.split(",")) == 1:
                self.countryName = countryName
        except Exception:
            try:
                countryName = _BeautifulSoup(_get(f"https://github.com/{self.username}",
                                                  headers={"User-Agent": user_agent.generate_user_agent()}).text,
                                             "html.parser").find("li", attrs={"itemprop": "homeLocation"}).find("span",
                                                                                                                attrs={
                                                                                                                    "class": "p-label"}).text
                if len(countryName.split(",")) == 2:
                    self.countryName = countryName.split(",")[1]
                elif len(countryName.split(",")) == 1:
                    self.countryName = countryName
                else:
                    self.countryName = None
            except (AttributeError, IndexError):
                self.countryName = None

        if self.username.strip() == "":
            print("Github username must NOT be empty.")

        if self.__resp["email"] is not None:
            self.email = self.__resp["email"]
        else:
            self.email = self.userEmail()
        # try:
        #     self.followers = self.__resp["followers"]
        # except:
        #     self.followers = None

        try:
            self.rep_os = self.__resp["public_repos"]
        except:
            self.rep_os = None

        self.CURRENT_PATH = _os.getcwd()

        ##################################### Followers Response #####################################

        self.__followersResp = _BeautifulSoup(_get(f"https://github.com/{self.username}?tab=followers").text,
                                              "html.parser")
        followers = self.__followersResp.find("span", attrs={"class": "text-bold color-text-primary"}).text

        if followers.endswith("k"):
            self.followers = float(followers.strip("k")) * 1000
        else:
            self.followers = int(followers)

        ##################################### Following Response #####################################
        self.__followingResp = _BeautifulSoup(_get(f"https://github.com/{self.username}?tab=following").text,
                                              "html.parser")
        following = self.__followingResp.findAll("span", attrs={"class": "text-bold color-text-primary"})[1].text

        if following.endswith("k"):
            self.following = float(following.strip("k")) * 1000
        else:
            self.following = int(following)

        self.__resp2 = _BeautifulSoup(_get(f"https://github.com/{username}").text, "html.parser")

        self.fullName = str(
            self.__resp2.find("span", attrs={"class": "p-name vcard-fullname d-block overflow-hidden"}).text).strip()

        try:
            self.location = self.__resp2.find("span", attrs={"class": "p-label"}).text
        except:
            self.location = None

        try:
            self.rating = int(self.__resp2.find("span", attrs={"class": "text-bold color-text-primary"}).text)
        except:
            self.rating = None
        # try:
        #     self.blog = self.__resp2.findAll("a", attrs={"class": "Link--primary"})[-4].text
        # except:
        #     self.blog = None

    def getFollowersImgs(self):
        folloersImgsAttrs = {"class": "d-table table-fixed col-12 width-full py-4 border-bottom color-border-secondary"}

        followersImgsLinksList = []
        for pageNum in range(1, _ceil(self.followers / 50) + 1):
            if pageNum == 1:
                soup = _BeautifulSoup(_get(f"https://github.com/{self.username}?&tab=followers").text,
                                      "html.parser")
            else:
                soup = _BeautifulSoup(
                    _get(f"https://github.com/{self.username}?page={str(pageNum)}&tab=followers").text,
                    "html.parser")

            followersContainer = soup.findAll("div", attrs=folloersImgsAttrs)

            for followerTag in followersContainer:
                # print(followerTag.find("img", attrs={"class": "avatar avatar-user"})["src"][:-10])
                followersImgsLinksList.append(
                    followerTag.find("img", attrs={"class": "avatar avatar-user"})["src"][:-10])

        return followersImgsLinksList

    def __createPathAndEnterIn(self, Path):
        if not _os.path.exists(Path):
            _os.mkdir(Path)
        _os.chdir(Path)

    def fetchInfo(self) -> tuple:
        """ Method For Collecting All user info such as his followers number, email, full name and more """
        res = self.__resp  # API request.
        # ################################################# Begin User Info
        # ##################################################

        """ ############# """

        """ For Test """
        # def info(query):
        #     return res[query]

        """ ############# """
        userInfo = {}  # Dictionary to store user info.
        """

        user_id = res["id"]
        profile_pic = res["avatar_url"]
        followers_url = res["followers_url"]
        following_url = res["following_url"]
        rep_os_url = res["rep_os_url"]
        length_of_rep_os = len(rep_os_url)
        name = res["name"]
        company = res["company"]
        blog = res["blog"]
        location = res["location"]
        email = res["email"]
        hireable = res["hireable"]
        bio = res["bio"]
        twitter_username = res["twitter_username"]
        puplic_rep_os = res["public_rep_os"]
        followes = res["followers"]
        following = res["following"]
        created_at = res["created_at"]
        last_Update = res["updated_at"]

        """
        """
        userInfo.update({
            "user_id": user_id,
            "profile_pic": profile_pic,
            "followers_url": followers_url,
            "following_url": following_url,
            "rep_os_url": rep_os_url,
            "length_of_rep_os": length_of_rep_os,
            "name": name,
            "company": company,
            "blog": blog,
            "location": location,
            "email": email,
            "hireable": hireable,
            "bio": bio,
            "twitter_username": twitter_username,
            "puplic_rep_os": puplic_rep_os,
            "followes": followes,
            "following": following,
            "created_at": created_at,
            "last_Update": last_Update
        }) """  # Append data to userInfo Dictionary.

        ############################################## End User Info ##############################################
        return res

    def countryinfo(self):
        """ A simple function to collect information about any country """
        if self.countryName is None:
            return None
        try:
            country = _countryinfo.CountryInfo(self.countryName)
            countryinfo = country.info()
        except:
            return None
        return countryinfo

    def downloadProfilePic(self, user=None, Path=current_path):
        """ Method for downloading specific  profile picture of Github user or Id
         You can specify the path for downloading the picture, default is current path.
         """
        if user is None:  # download object profile picture.
            user = self.username
            picUrl = f"https://avatars.githubusercontent.com/u/{self.__resp['id']}?v=4"  # The profile pic of the
            # object or instance.
        else:  # download the profile picture of another user
            picUrl = _BeautifulSoup(_get(f"https://github.com/{user}", headers=self.__headers).text,
                                    "html.parser").find("img", attrs={
                "class": "avatar avatar-user width-full border color-bg-primary"})["src"]

        self.__createPathAndEnterIn(Path)
        picName = user + ".jpeg"

        if not _pathlib.Path(picName).exists():
            _urlretrieve(picUrl, picName)
        _os.chdir(self.CURRENT_PATH)

        return _os.path.abspath(_os.path.join(Path, picName))

    """
    # def downloadAllProfPics(self, path=current_path):
    #     Method for downloading specific number of profile pictures of Github users 
    #     # if not _os.path.exists(path):
    #     #     _os.mkdir(path)
    #     #
    #     # _os.chdir(path)
    #
    #     pass
    """

    def getProfileById(self, UserId: str) -> str:
        """ Method that gets the user link profile by his Github id """
        api = f"https://api.github.com/user/{UserId}"  # API for return user info by ID.
        profileLink = _get(api).json()["html_url"]
        return profileLink

    def fetch(self):
        """ Method For Collecting All user info such as his followers number, email, full name and more """
        api = f"https://api.github.com/users/{self.username}"

        token = "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"

        headersDic = {
            "Authorization": f"token {token}"
        }
        resp = _get(api, headers=headersDic).json()
        if resp["message"] == 'Bad credentials':
            return self.fetchInfo()
        return resp

    def getFollowersProfiles(self) -> list:
        """ Simple method for fetching followers urls """
        return [f"https://github.com/{followerUsername}" for followerUsername in self.getFollowersUsernames()]

    def getFollowingProfiles(self) -> list:
        return [f"https://github.com/{followingUsername}" for followingUsername in self.getFollowingUsernames()]

    def getFollowingImgs(self) -> list:
        """ _get All Following Pictures """

        followingImgsAttrs = {
            "class": "d-table table-fixed col-12 width-full py-4 border-bottom color-border-secondary"}

        followingImgsLinksList = []
        for pageNum in range(1, _ceil(self.following / 50) + 1):
            if pageNum == 1:
                soup = _BeautifulSoup(_get(f"https://github.com/{self.username}?&tab=following").text,
                                      "html.parser")
            else:
                soup = _BeautifulSoup(
                    _get(f"https://github.com/{self.username}?page={str(pageNum)}&tab=following").text,
                    "html.parser")

            followingContainer = soup.findAll("div", attrs=followingImgsAttrs)

            for followerTag in followingContainer:
                followingImgsLinksList.append(
                    followerTag.find("img", attrs={"class": "avatar avatar-user"})["src"][:-10])

        return followingImgsLinksList

    def downloadFollowersPics(self, Path=current_path):
        """ Method for downloading followers profile phot_os  """

        self.__createPathAndEnterIn(Path)

        followersProfilesPicsList = self.getFollowersImgs()
        followersUsernames = self.getFollowersUsernames()

        """ Downloading Profiles Pictures """
        for imageLink, followerUsername in zip(followersProfilesPicsList, followersUsernames):
            # imgName = (str(imageLink).split("/")[-1])[:-4] + ".jpeg"
            imgName = followerUsername + ".jpeg"  # profile picture will be named with it's owner.
            if not _pathlib.Path(imgName).exists():
                _urlretrieve(imageLink, imgName)
        _os.chdir(self.CURRENT_PATH)

    def downloadFollowingPics(self, Path=current_path):
        """ Method for downloading following profile phot_os  """
        self.__createPathAndEnterIn(Path)

        followingsProfilesPicsList = self.getFollowingImgs()
        followingUsernames = self.getFollowingUsernames()
        """ Downloading Profiles Pictures """
        for imageLink, followingUsername in zip(followingsProfilesPicsList, followingUsernames):
            # imgName = (str(imageLink).split("/")[-1])[:-4] + ".jpeg"
            imgName = followingUsername + ".jpeg"  # profile picture will be named with it's owner.
            if not _pathlib.Path(imgName).exists():
                _urlretrieve(imageLink, imgName)

        _os.chdir(self.CURRENT_PATH)

    def __path__(self):
        return _os.path.abspath(__file__)

    # def getFollowersEmails(self) -> list:
    #     followersEmails = []
    #     for followerData in _get(self.__resp["followers_url"], headers=self.__headersDic).json():
    #         try:
    #             followersEmails.append(_get(followerData["url"], headers=self.__headersDic).json()["email"])
    #             # print(followerData["login"]["email"])
    #             # print(_get(followerData["url"]).json()["email"])
    #         except:
    #             pass
    #     return followersEmails

    # def getFollowingEmails(self) -> list:
    #     followingEmails = []
    #     for followingData in _get(self.__resp["following_url"], headers=self.__headersDic).json():
    #         try:
    #             followingEmails.append(_get(followingData["url"], headers=self.__headersDic).json()["email"])
    #             # print(_get(followingData["url"]).json()["email"])
    #             # print(followingData)
    #         except:
    #             pass
    #     return followingEmails

    def userEmail(self, user=None):
        """
        :return email of a specific user if provided
        otherwise returns the email of object
        """
        if user is None:
            user = self.username
        soup = _BeautifulSoup(_get(f"https://github.com/{user}", headers=self.__headers).text, "html.parser")
        try:
            userEmail = soup.find('a', {"class": "u-email Link--primary"}).text
        except AttributeError:  # email is NOT provided.
            userEmail = None

        return userEmail

    def allEmails(self, user=None) -> list:
        """
        :return all available emails of a specific user if provided
        otherwise returns the email of object's user.
        """
        if user is None:
            user = self.username
        emails = [emailTag["href"][7:] for emailTag in _BeautifulSoup(
            _get(f"https://github.com/{user}", headers={"User-Agent": user_agent.generate_user_agent()}).text,
            "html.parser").select("a[href ^= 'mailto:']")]
        return emails

    def extLinks(self, user=None) -> list:
        """ :return the external links of Github user
        if user argument is None method will return t-
        he external links of object's user.
        """
        if user is None:
            user = self.username

        extLinks = [aTag["href"] for aTag in
                    _BeautifulSoup(_get(f"https://github.com/{user}",
                                        headers={"User-Agent": user_agent.generate_user_agent()}).text,
                                   "html.parser").find(
                        "div", attrs={"class": "js-profile-editable-area d-flex flex-column d-md-block"}).find_all("a",
                                                                                                                   attrs={
                                                                                                                       "class": "Link--primary"})]
        return extLinks

    def getFollowersUsernames(self) -> list:
        """ get all followers usernames """

        followersUsernames = []

        for pageNum in range(1, _ceil(self.followers / 50) + 1):
            if pageNum == 1:
                soup = _BeautifulSoup(
                    _get(f"https://github.com/{self.username}?&tab=followers", headers=self.__headers).text,
                    "html.parser")
            else:
                soup = _BeautifulSoup(
                    _get(f"https://github.com/{self.username}?page={str(pageNum)}&tab=followers",
                         headers=self.__headers).text,
                    "html.parser")

            for followerUsernameTag in soup.find_all("span", attrs={"class": "Link--secondary"}):
                followersUsernames.append(followerUsernameTag.text)

        return followersUsernames

    # def getFollowersUsernames(self):
    #     _Thread(target=self._getFollowersUsernames).start()

    def getFollowersEmails(self, output=None) -> list:
        """get all followers emails"""

        followersUsernames = self.getFollowersUsernames()
        followersEmails = []
        for followerUsername in followersUsernames:
            followersEmails.append({followerUsername: self.userEmail(followerUsername)})

        # Saving emails inside an output file
        if output is not None:
            for followerEmail in followersEmails:
                with open(output, "a") as outputFile:
                    print(followerEmail, file=outputFile)
        return followersEmails

    def getFollowingUsernames(self) -> list:
        """get all following usernames"""

        followingUsernames = []

        for pageNum in range(1, _ceil(self.following / 50) + 1):
            if pageNum == 1:
                soup = _BeautifulSoup(
                    _get(f"https://github.com/{self.username}?&tab=following", headers=self.__headers).text,
                    "html.parser")
            else:
                soup = _BeautifulSoup(
                    _get(f"https://github.com/{self.username}?page={str(pageNum)}&tab=following",
                         headers=self.__headers).text,
                    "html.parser")

            for followingUsernameTag in soup.find_all("span", attrs={"class": "Link--secondary"}):
                followingUsernames.append(followingUsernameTag.text)

        return followingUsernames

    def getFollowingEmails(self, output=None) -> list:
        """get all following emails"""
        followingUsernames = self.getFollowingUsernames()
        followingEmails = []
        for followingUsername in followingUsernames:
            followingEmails.append({followingUsername: self.userEmail(followingUsername)})

        # Saving emails inside an output file
        if output is not None:
            for followingEmail in followingEmails:
                with open(output, "a") as outputFile:
                    print(followingEmail, file=outputFile)
        return followingEmails


"""
/* TESTING/DEBUGGING */
################################################## Begin User Info ##################################################

"""
# For Test """
# def info(query):
#     return res[query]


# USER_ID = res["id"]
# PROFILE_PIC = res["avatar_url"]
# FOLLOWERS_URL = res["followers_url"]
# FOLLOWING_URL = res["following_url"]
# REP_os_URL = res["rep_os_url"]
# LENGTH_OF_REP_os = len(REP_os_URL)
# NAME = res["name"]
# COMPANY = res["company"]
# BLOG = res["blog"]
# LOCATION = res["location"]
# EMAIL = res["email"]
# HIREABLE = res["hireable"]
# BIO = res["bio"]
# TWITTER_USERNAME = res["twitter_username"]
# PUPLIC_REP_os = res["public_rep_os"]
# FOLLOWES = res["followers"]
# FOLLOWING = res["following"]
# CREATED_AT = res["created_at"]
# LAST_UPDATE = res["updated_at"]

################################################## End User Info ##################################################

# print(USER_ID)
# print(PROFILE_PIC)
# print(FOLLOWERS_URL)
# print(FOLLOWING_URL)
# print(REP_os_URL)
# print(LENGTH_OF_REP_os)
# print(NAME)
# print(COMPANY)
# print(BLOG)
# print(LOCATION)
# print(EMAIL)
# print(HIREABLE)
# print(BIO)
# print(TWITTER_USERNAME)
# print(PUPLIC_REP_os)
# print(FOLLOWES)
# print(FOLLOWING)
# print(CREATED_AT)
# print(LAST_UPDATE)"""
