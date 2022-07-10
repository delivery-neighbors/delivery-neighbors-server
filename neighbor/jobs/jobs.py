from datetime import datetime

from django.db.models import Count
from django.utils.dateformat import DateFormat
from wordcloud import WordCloud

from neighbor.models import Search


def schedule_api():
    print("Every hour this executed")
    print(f"Now({datetime.now()}), wordcloud created!")

    top_search_instances = Search.objects.values('search_content').annotate(dcount=Count('search_content'))
    top_search_list = list(
        top_search_instances.order_by('-dcount')[:10])  # Search.objects.all().values('search_content')
    key, val = [], []
    for i in top_search_list:
        key.append(i['search_content'])
        val.append(i['dcount'])

    search_dict = dict(zip(key, val))

    wordcloud = WordCloud(
        font_path='./static/wordcloud/font/BMDOHYEON_ttf.ttf',
        background_color='white',
        colormap='summer',
        width=300,
        height=200,
    ).generate_from_frequencies(dict(search_dict))

    wordcloud.to_file(f'./static/wordcloud/images/wc_{DateFormat(datetime.now()).format("YmdHi")}.jpg')
