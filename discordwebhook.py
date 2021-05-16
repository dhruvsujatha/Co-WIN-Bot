from discord_webhook import DiscordWebhook, DiscordEmbed
import apirequest as ap
import time
import json

def sendwebhook(data, urlss): #Send Discord Notifications as Webhooks
    webhook = DiscordWebhook(url=urlss) #Get Webhook URLs
    embed = DiscordEmbed(title="New Vaccination Slot Found !", description="Here is a list of centers available", color=14973201)    
    embed = DiscordEmbed(title="New Vaccination Slot Found !", description="Here is a list of centers available", color=14973201)    
    embed.set_author(name='Dhruv Sujatha')
    embed.set_footer(text='Live data updated at')
    embed.set_timestamp()
    embed.add_embed_field(name='Name', value=data["name"] ,inline=False)
    embed.add_embed_field(name='Area', value=data["block_name"] ,inline=False)
    embed.add_embed_field(name='Pincode', value=data["pincode"], inline=False)
    embed.add_embed_field(name='Vaccine', value=data["vaccine"] ,inline=False)
    embed.add_embed_field(name='Age Group', value="18 - 45" ,inline=False)
    embed.add_embed_field(name='Date', value=data["date"] ,inline=False)
    embed.add_embed_field(name='Slot Available Time', value=data["from"]+" to "+data["to"] ,inline=False)
    embed.add_embed_field(name='Fee Type', value=data["fee_type"] ,inline=False)
    embed.add_embed_field(name='No of Vaccines available ', value=data["available_capacity"] ,inline=False)
    webhook.add_embed(embed)
    response = webhook.execute(remove_embeds=True, remove_files=True)
    print("Webook Successfully Sent to ",urlss)
    time.sleep(1)

urlss = 'https://discord.com/api/webhooks/843163876488118273/keN5f6orbIL23atTyHD9S50QPH24sXNbbJY1r1qnXJ7HRREX1rlZrhZyi8UD1OLUhJiM'

l = []

while True:
    counter = 0
    co = ap.CoWinAPI()
    try: 
        if counter <=2:
            resp = co.protectedapi(district_id = 571)
            data = ap.dataSel(resp, 18).dataSelection()
        else:
            resp = co.publicapi(district_id = 571)
            data = ap.dataSel(resp, 18).dataSelection()
    except json.decoder.JSONDecodeError:
        print("Error Getting JSON from COWIN")
        counter+=1

    print(json.dumps(data, indent = 1))

    for i in range(0, len(data['centers'])):
        if data['centers'][i] not in l:
            l.append(data['centers'][i])
            a = data['centers'][i]
            sendwebhook(a, urlss)

    for i in l:
        if i not in ap.currentresp(data):
            l.remove(i)
    
    time.sleep(120)