import requests
import json 
from bs4 import BeautifulSoup

city=input("Entrez la ville : ")
typeAchat=input("Entrez le type d'achat , exemple ( maison / appartement / terrain / chateau ... ) : ")
typeAnciennete=input("Cherchez vous un programme neuf ou ancien ? : ")


file= open("main.html", "w")
file.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Nexity scraping </title>
</head>

<body >''')

for counter in range(10, 110, 10):

    page = requests.get(f'https://www.nexity.fr/annonces-immobilieres/achat-vente/{typeAchat}/{typeAnciennete}/{city}')

    soupdata = BeautifulSoup(page.content, "html.parser")

    results = soupdata.find_all("div", class_="ais-hits--item")

    for result in results:
        contentAnnonce = result.find("div" , class_="content-annonce")
        image = result.find("img")["src"]
        location = result.find("div", class_="sub-title")
        salary = result.find("div", class_="inter-description")
        company = result.find("a", class_="offer-link")
        title = result.find("div", class_="title")
        titleText = title.text
        if title.text[:7] == "nouveau":
            titleText=(title.text[7:])
        file.write(f'''
            <div class="card m-4 p-2 m-auto  border border-primary" style="width: 50rem;">
                <div class="card-body">
                    <img  src="{image}" alt="Card image cap" style="width:100px; height:100px">
                    <p class="card-text  "><span class="text-danger">Les informations de l'annonce : </span>{contentAnnonce.text}</p>
                    <h5 class="card-title btn btn-primary">{titleText}</h5>
                </div>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item"><span class="text-primary">Localisation  </span>{location.text}</li>
                    <li class="list-group-item text-success"> À partir de : {f' {salary.text}</li>' if salary else ""}
                </ul>
            </div>   
  ''')

file.write('''
</body>
</html>''')