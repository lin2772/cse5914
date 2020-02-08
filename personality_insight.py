from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname
import json

authenticator = IAMAuthenticator('{key}')#key
personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    authenticator=authenticator
)
# request url
personality_insights.set_service_url('{url}')
#location of plot.txt
fileLocation = '{file location}'
f= open(fileLocation,"r")
fout = open("result.txt","w+")
Lines = f.readlines()
count = 0
# Strips the newline character
for line in Lines:
    plot_index = [i for i in range(len(line)) if line.startswith('plot":"', i)]    #get the index of plot
    list_id_index = [i for i in range(len(line)) if line.startswith('netflixid":"', i)] #get the index of netflex id
    index_num_s = list_id_index[0]+12
    index_num_e = line.find('"', index_num_s)
    id = line[index_num_s:index_num_e]
    fout.write(line[index_num_s:index_num_e]+'\n')
    print(id)
    if(len(plot_index)>0):
        plot_s = plot_index[0] + 7
        plot_e = line.find('"', plot_s)
        plot = line[plot_s:plot_e]
        if(len(plot)> 200):
            # copy 5 time
            plot = plot+plot+plot+plot+plot+'\n'
            profile = personality_insights.profile(
                    plot,
                    'application/json',
                    content_type='text/plain',
                    consumption_preferences=True,
                    raw_scores=False
            ).get_result()
            fout.write(json.dumps(profile, indent=2))
        #record the total number of request made
        count= count+1
    if(count>=1000):
        break

f.close()
fout.close()

#print(json.dumps(profile, indent=2))
