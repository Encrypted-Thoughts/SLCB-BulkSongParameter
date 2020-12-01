# SLCB Bulk Song Parameter

The Bulk Song Parameter allows for creating custom commands to add batches of songs from playlist to song queue.
This is achieved by creating csv files populated with the titles of the songs to be added and saved at the BuilkSongParameter\Song Lists under the script installation folder.

## Installing

This script was built for use with Streamlabs Chatbot.
Follow instructions on how to install custom script packs at:
https://github.com/StreamlabsSupport/Streamlabs-Chatbot/wiki/Prepare-&-Import-Scripts

Click [Here](https://github.com/Encrypted-Thoughts/SLCB-BulkSongParameter/releases/download/v1.0/BulkSongParameter.zip) to download the script pack.

## Use

Once installed the below parameter can be inserted into custom commands created in SLCB.
```
$addsongs(
    string  # File Name: The name of the csv file containing song title to be added.
)

Example Command: !command add !lofi $addsongs(lofi)
Example Command: !command add !rock $addsongs(rock)
```

## Author

EncryptedThoughts - [Twitch](https://www.twitch.tv/encryptedthoughts)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
