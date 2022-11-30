# -*- coding: utf-8 -*-

#We create an array with the different products
products = ["gasoline_95E5", 
            "gasoline_95E5_premium ", 
            "gasoline_98E5",
            "gasoline_98E10",
            "diesel_A",
            "diesel_B",
            "diesel_premium",
            "bioetanol",
            "biodiesel",
            "lpg",
            "cng",
            "lng",
            "hydrogen"]

#We observe the different types of schedules and we range them

# print(df['schedule'].unique())
# print(df.groupby('schedule').count())

# We create a dictionary with the shedule values in order to classify them.
schedule_dict = {
        
        "L-D: 05:00-23:00"                                  : "L-D",                                           
        "L-D: 05:59-23:59"                                  : "L-D",                                      
        "L-D: 06:00-00:00"                                  : "L-D",                                       
        "L-D: 06:00-01:30"                                  : "L-D",                                         
        "L-D: 06:00-22:00"                                  : "L-D",                                         
        "L-D: 06:00-23:00"                                  : "L-D",                                          
        "L-D: 06:00-23:59"                                  : "L-D",                                           
        "L-D: 06:30-22:30"                                  : "L-D",                                           
        "L-D: 07:00-21:30"                                  : "L-D",                                           
        "L-D: 07:00-23:00"                                  : "L-D",                                           
        "L-D: 12:00-20:00"                                  : "L-D",                                           
        "L-D: 24H"                                          : "24H",                                          
        "L-J: 06:30-23:00; V: 06:45-22:45; S: 06:45-14:45"  : "L-D",         
        "L-S: 00:00-14:00"                                  : "L-S",                                          
        "L-S: 06:00-22:00"                                  : "L-S",                                         
        "L-S: 06:30-21:30; D: 08:00-14:00"                  : "L-D",                           
        "L-S: 07:00-19:00"                                  : "L-S",                                         
        "L-S: 07:00-21:00"                                  : "L-S",                                       
        "L-S: 07:00-21:00; D: 09:00-14:00"                  : "L-D",                          
        "L-S: 07:00-21:00; D: 9:00-14:00"                   : "L-D",         
        "L-V: 06:00-21:00"                                  : "L-V",           
        "L-V: 06:00-21:00; S: 08:00-20:00; D: 09:00-15:00"  : "L-D",      
        "L-V: 06:00-22:00; S-D: 08:00-20:00"                : "L-D",           
        "L-V: 06:00-22:00; S-D: 10:00-19:00"                : "L-D",           
        "L-V: 06:00-22:00; S: 07:00-15:00"                  : "L-S",           
        "L-V: 06:00-22:00; S: 07:00-15:00; D: 08:00-16:00"  : "L-D",           
        "L-V: 06:00-23:45; S-D: 07:00-23:00"                : "L-D",           
        "L-V: 07:00-21:00; S: 08:00-14:00"                  : "L-S",           
        "L-V: 07:00-21:00; S: 08:00-14:30; D: 09:00-15:00"  : "L-D",           
        "L-V: 07:00-21:00; S: 09:00-14:00"                  : "L-S",           
        "L-V: 07:00-21:00; S: 09:00-15:00"                  : "L-S",           
        "L-V: 07:00-21:00; S: 09:30-14:30"                  : "L-S",           
        "L-V: 07:00-21:30; S: 07:00-14:00"                  : "L-S",           
        "L-V: 07:00-21:30; S: 08:00-15:00"                  : "L-S",           
        "L-V: 07:00-21:30; S: 08:00-15:30"                  : "L-S",           
        "L-V: 07:00-21:30; S: 09:00-14:00"                  : "L-S",           
        "L-V: 07:00-21:45; S: 08:15-13:45"                  : "L-S",           
        "L-V: 07:00-22:00; S-D: 09:00-21:00"                : "L-D",           
        "L-V: 07:00-22:00; S: 08:00-15:00"                  : "L-S",           
        "L-V: 07:00-22:00; S: 08:00-21:00"                  : "L-S",           
        "L-V: 07:00-22:00; S: 09:00-14:00"                  : "L-S",           
        "L-V: 07:00-22:00; S: 09:00-15:00"                  : "L-S",           
        "L-V: 07:30-20:30; S: 08:00-14:00"                  : "L-S",           
        "L-V: 07:30-21:00; S: 07:30-14:30; D: 09:00-14:00"  : "L-D",           
        "L-V: 07:30-21:00; S: 08:00-14:30"                  : "L-S",           
        "L-V: 07:30-21:00; S: 08:00-15:00; D: 09:00-15:00"  : "L-D",           
        "L-V: 07:30-21:00; S: 08:30-14:45"                  : "L-S",           
        "L-V: 07:30-21:00; S: 09:30-14:30"                  : "L-S",           
        "L-V: 07:30-21:30; S: 08:00-15:00"                  : "L-S",           
        "L-X: 07:00-23:00; J: 07:00-23:59; V-S: 00:00-23:59; D: 00:00-23:00": "L-D",           
        "L: 24H"                                            : "L"  ,         
        "S: 08:00-15:00"                                    : "S"          
                
        }

  
# create a new column based on condition
df['schedule_parsed'] = df['schedule'].map(schedule_dict)

# Because we have selected only oil stations in Madrid, the columns about 
# municipality, region, province, town are reduntant

df = df.drop(columns=['province_name', 
                      'region_name',
                      'municipality_id',
                      'municipality_name',
                      'province_id',
                      'region_id',
                      'town'])

#We separate the dataset depending on the oil availability in order to 
# train the different models.

products = ["gasoline_95E5", 
            "gasoline_95E5_premium ", 
            "gasoline_98E5",
            "gasoline_98E10",
            "diesel_A",
            "diesel_B",
            "diesel_premium",
            "bioetanol",
            "biodiesel",
            "lpg",
            "cng",
            "lng",
            "hydrogen"]

df_gasoline_95E5 = df.where(df['gasoline_95E5']!=0)
df_gasoline_95E5_premium = df.where(df['gasoline_95E5_premium']!=0)
df_gasoline_98E5 = df.where(df['gasoline_98E5']!=0)
df_gasoline_98E10 = df.where(df['gasoline_98E10']!=0)
df_diesel_A = df.where(df['diesel_A']!=0)
df_diesel_B = df.where(df['diesel_B']!=0)
df_diesel_premium = df.where(df['diesel_premium']!=0)
df_bioetanol = df.where(df['bioetanol']!=0)
df_biodiesel = df.where(df['biodiesel']!=0)
df_lpg = df.where(df['lpg']!=0)
df_cng = df.where(df['cng']!=0)
df_lng = df.where(df['lng']!=0)
df_hydrogen = df.where(df['hydrogen']!=0)




