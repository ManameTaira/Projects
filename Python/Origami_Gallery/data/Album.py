class albumData:

    Collection = {
       0:{
           "img_name":"SS_6a.jpg",
        "img_path":"imagens/",
        "date":"2020-05-08",
        "tag":"Composição",
        "carrossel":True,
        "comment":False,
        "comment_txt":"Tsurus feitos em papel de origami, suporte feito a partir de um galho de bambu, a base feita de cano pvc.",
        "img":"SS_6a.jpg,SS_6b.jpg,SS_6c.jpg"},

        1:{"img_name":"U_5.jpg",
        "img_path":"imagens/",
        "date":"2020-05-04",
        "tag":"Simples",
        "carrossel":False,
        "comment":False,
        "comment_txt":"",
        "img":"U_5.jpg"},

        2:{"img_name":"U_8.jpg",
        "img_path":"imagens/",
        "date":"2019-12-11",
        "tag":"Flower",
        "carrossel":False,
        "comment":False,
        "comment_txt":"",
        "img":"U_8.jpg"},

        3:{"img_name":"U_6.jpg",
        "img_path":"imagens/",
        "date":"2019-11-24",
        "tag":"Flower",
        "carrossel":False,
        "comment":False,
        "comment_txt":"Rosas em papel de origami, vaso feito em rolha de vinho",
        "img":"U_6.jpg"},

        4:{"img_name":"U_4.jpg",
        "img_path":"imagens/",
        "date":"2019-11-10",
        "tag":"Flower",
        "carrossel":False,
        "comment":False,
        "comment_txt":"",
        "img":"U_4.jpg"},

        5:{"img_name":"U_3.jpg",
        "img_path":"imagens/",
        "date":"2018-09-01",
        "tag":"Flower",
        "carrossel":False,
        "comment":False,
        "comment_txt":"",
        "img":"U_3.jpg"},

        6:{"img_name":"U_2.jpg",
        "img_path":"imagens/",
        "date":"2018-08-10",
        "tag":"Flower",
        "carrossel":False,
        "comment":False,
        "comment_txt":"",
        "img":"U_2.jpg"},

        7:{"img_name":"SS_1a.jpg",
        "img_path":"imagens/",
        "date":"2018-07-22",
        "tag":"Kusudama",
        "carrossel":True,
        "comment":False,
        "comment_txt":"",
        "img":"SS_1a.jpg,SS_1b.jpg,SS_1c.jpg"},

        8:{"img_name":"U_1.jpg",
        "img_path":"imagens/",
        "date":"2018-05-30",
        "tag":"Flower",
        "carrossel":False,
        "comment":False,
        "comment_txt":"",
        "img":"U_1.jpg"},

        9:{"img_name":"SS_5a.jpg",
        "img_path":"imagens/",
        "date":"2018-04-23",
        "tag":"Flower",
        "carrossel":True,
        "comment":False,
        "comment_txt":"",
        "img":"SS_5a.jpg,SS_5b.jpg"},

        10:{"img_name":"SS_4a.jpg",
        "img_path":"imagens/",
        "date":"2018-04-05",
        "tag":"Flower",
        "carrossel":True,
        "comment":False,
        "comment_txt":"",
        "img":"SS_4a.jpg,SS_4b.jpg"},

        11:{"img_name":"SS_3a.jpg",
        "img_path":"imagens/",
        "date":"2018-02-18",
        "tag":"Flower",
        "carrossel":True,
        "comment":False,
        "comment_txt":"",
        "img":"SS_3a.jpg,SS_3b.jpg"},

        12:{"img_name":"SS_2a.jpg",
        "img_path":"imagens/",
        "date":"2018-02-02",
        "tag":"Kusudama",
        "carrossel":True,
        "comment":False,
        "comment_txt":"",
        "img":"SS_2a.jpg,SS_2b.jpg,SS_2c.jpg"},

        13:{"img_name":"U_7.jpg",
        "img_path":"imagens/",
        "date":"2018-01-28",
        "tag":"Flower",
        "carrossel":False,
        "comment":False,
        "comment_txt":"",
        "img":"U_7.jpg"},

        14:{"img_name":"U_9.jpg",
        "img_path":"imagens/",
        "date":"2018-01-25",
        "tag":"Flower",
        "carrossel":False,
        "comment":True,
        "comment_txt":"PatinhoFeio",
        "img":"U_9.jpg"},

        15:{"img_name":"SS_8a.jpg",
        "img_path":"imagens/",
        "date":"2020-07-17",
        "tag":"Flower",
        "carrossel":True,
        "comment":True,
        "comment_txt":"",
        "img":"SS_8a.jpg,SS_8b.jpg"}
       }

class month_pt:
    name = ("Janeiro",
             "Fevereiro",
             "Março",
             "Abril",
             "Maio",
             "Junho",
             "Julho",
             "Agosto",
             "Setembro",
             "Outubro",
             "Novembro",
             "Dezembro")
class month_en:
    name = ("January",
             "February",
             "March",
             "April",
             "May",
             "June",
             "July",
             "August",
             "September",
             "October",
             "November",
             "December")

def sort_by_data(collection):

    date = []
    index = []
    for i in collection:
        date.append(collection[i]["date"])
        index.append(i)

    zipped_lists = zip(date, index)
    sorted_pairs = sorted(zipped_lists,reverse=True)

    data_list = zip(*sorted_pairs)
    index_sort = []
    for i in sorted_pairs:
        index_sort.append(i[1])
    return index_sort
