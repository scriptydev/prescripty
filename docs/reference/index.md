# Commands

!!! info
    Required parameters are surrounded by `[]`. Optional arguments are wrapped using `()`.

!!! danger
    Do not literally type out `[]` or `()`!

!!! tip
    Parameters in a correctly formed command might look similar to `/command [[option] value]` in the user interface.

## **Fun**

### `activity`

`Slash Command`

Start a Discord Activity

**Parameters**  
`[activity]` Activity to start  

```python
ACTIVITIES = {
    "Poker Night": "755827207812677713",
    "Chess In The Park": "832012774040141894",
    "Letter League": "879863686565621790",
    "SpellCast": "852509694341283871",
    "Watch Together": "880218394199220334",
    "Checkers In The Park": "832013003968348200",
    "Word Snacks": "879863976006127627",
    "Blazing 8s": "832025144389533716",
    "Sketch Heads": "902271654783242291",
    "Land-io": "903769130790969345",
    "Betrayal.io": "773336526917861400",
    "Fishington.io": "814288819477020702",
    "Putt Party": "945737671223947305",
}
```  

`[channel]` Channel for activity

!!! note
    The `[activity]` option returns an autocomplete interaction interface. From the panel pop up, you can select and search the Activity to start or enter a valid Discord Activity Application ID. **==By default, only ^^10 activity choices^^ are shown at once! Please type to search for the activity if it does not appear by default.==**

### `animal cat`

`Slash Command`

Get a random cat image

### `animal dog`

`Slash Command`

Get a random dog image

### `coin`

`Slash Command`

Flip a coin

### `dice`

`Slash Command`

Roll a dice

### `meme`

`Slash Command`

The hottest Reddit rmemes

### `rickroll`

`Slash Command`

;)

### `rps`

Play rock paper scissors

## **Help**

### `help`

`Slash Command`

Display the help interface

## **Misc**

### `Avatar`

`Context Menu`

Get user avatar

### `echo`

`Slash Command`

Repeats user input

**Parameters**  
`[text]` Text to repeat

### `poll`

`Slash Command`

Create a simple poll

**Parameters**  
`[topic]` Topic of the poll  
`[option_a]` Option A  
`[option_b]` Option B  
`(option_c)` Option C  
`(option_d)` Option D  
`(option_e)` Option E  
`(option_f)` Option F  
`(option_g)` Option G  
`(option_h)` Option H  
`(option_i)` Option I  
`(option_j)` Option J

### `Translate to English`

`Context Menu`

Translate message to English

### `translate`

`Slash Command`

Translate message to specified language

**Parameters**  
`[text]` Text to translate  
`(source = auto)` Language to translate from  
`(target = en)` Language to translate to

## **Mod**

### `ban`

`Slash Command`

Ban user from server

**Parameters**  
`[user]` User to ban  
`(delete_message_days)` Days to delete user messages  
`(reason)` Reason for ban

### `delete`

`Slash Command`

Purge messages from channel

**Parameters**  
`[amount]` Amount to delete

### `kick`

`Slash Command`

Kick member from server

**Parameters**  
`[member]` Member to kick  
`(reason)` Reason for kick

### `slowmode enable`

`Slash Command`

Enable slowmode for channel

**Parameters**  
`[duration]` Duration of slowmode  
`(channel)` Channel to enable slowmode

### `slowmode disable`

`Slash Command`

Disable slowmode for channel

**Parameters**  
`(channel)` Channel to disable slowmode

### `timeout set`

`Slash Command`

Set timeout for member

**Parameters**  
`[member]` Member to timeout  
`[duration]` Duration of timeout  
`(reason)` Reason for timeout

### `timeout remove`

`Slash Command`

Remove timeout from member

**Parameters**
`[member]` Member to remove timeout

### `unban`

`Slash Command`

Unban user from server

**Parameters**
`[user]` User to unban

!!! note
    The `[user]` option returns an autocomplete interaction interface. You can select the user you want to unban or search by username as well as ID.

## **Util**

### `info channel`

`Slash Command`

Get information about channel

**Parameters**  
`(channel)` The channel to get information about

### `info invite`

`Slash Command`

Get information about invite

**Parameters**  
`(invite)` The invite to get information about

### `info role`

`Slash Command`

Get information about role

**Parameters**  
`[role]` The role to get information about

### `info server`

`Slash Command`

Get information about server

### `info user`

`Slash Command`

Get information about user

**Parameters**  
`[user]` The user to get information about

### `stats about`

`Slash Command`

About the Scripty Discord bot

### `stats ping`

`Slash Command`

Replies with bot latency

### `stats system`

`Slash Command`

Bot system information
