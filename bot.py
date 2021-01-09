from pyrogram import Client, types
import os
import time
import db


shedule_time = list(map(float, db.get_settings()[3].split()))
chat_id = -1001216485269
GTM = 0


def check(dir_name):
    if not dir_name in os.listdir():
        os.mkdir(dir_name)
        print("Папка " + dir_name + " создана успешно")
    else:
        print("Папка " + dir_name + " уже существует")


check("source")
check("complete")

last = db.get_last_message()[1]

minute = 60
hour = minute * 60
day = hour * 24

t = int(time.time())

next_day = int(t + day - t % day - hour * 3)
time_start = db.get_settings()[4]
caption = db.get_settings()[2]
shedule_time_unix = shedule_time[:]

time_start_unix = int(next_day - 24 * hour) + int(str(time_start).split(".")[0]) * hour + int(str(time_start).split(".")[1]) * minute + GTM * hour

if int(last) < int(next_day) and t > time_start_unix:
    for day in range(db.get_settings()[1]):
        print("\n\nЗапланировано постов - {}:".format(len(shedule_time)))
        for i in range(len(shedule_time)):
            print(
                "{} - {}".format(i + 1, '%.2f' % shedule_time[i]))

        for i in range(len(shedule_time)):
            shedule_time_unix[i] = next_day + int(str(shedule_time[i]).split(".")[0]) * hour + int(str('%.2f' % shedule_time[i]).split(".")[1]) * minute + GTM * hour + day * 24 * hour

        if len(os.listdir("source")) < len(shedule_time):
            print("{} файлов в папке, а публикаций запланированно {}".format(len(os.listdir("source")), len(shedule_time)))
            exit()

        app = Client("my_account")
        app.start()

        source_list = os.listdir("source")
        for i in range(len(shedule_time)):
            if len(source_list[i]) > 4 and source_list[i][-4:] == '.gif':
                app.send_document(chat_id=chat_id, document='source//{}'.format(source_list[i]), caption=caption, schedule_date=shedule_time_unix[i])
            else:
                path = 'source\\{}'.format(source_list[i])
                photo_list = os.listdir(path)
                photo_media = [types.InputMediaPhoto(media='{}\\{}'.format(path, photo_list[x]), caption=caption if x == 0 else '') for x in
                               range(len(photo_list))]
                app.send_media_group(chat_id=chat_id, media=photo_media, schedule_date=shedule_time_unix[i])
            os.rename("source\\{}".format(source_list[i]), "complete\\{}".format(source_list[i]))

        app.stop()



        db.edit_last_message(next_day+day*24*hour)
else:
    print("Еще рано, пропускаю выполнение")
time.sleep(5)

