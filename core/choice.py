LIST_CATEGORY_TYPE  =  (
                  ("video","Video"),
                  ("job","Job"),
                  ("event","Event"),
                  ("institute","Institute"),
                  ("article","Article"),
                 )

FLAG  =  ((1, "YES"), (0, "NO"))

def year_choice():
    import datetime
    now = datetime.datetime.now()
    current_year = now.year+5
    year_list = [(current_year-i,current_year-i) for i in range(211)]
    return year_list

LIST_YEAR  =  year_choice()

JOB_SITE_TYPE  =  (
                  ("monster","monster"),
                  ("naukri","naukri"),
                  ("government","government"),
                  ('other','other'),
                 )

