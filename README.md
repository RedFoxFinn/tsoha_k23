# ChatList

[![Pylint](https://github.com/RedFoxFinn/ChatList/actions/workflows/lint.yml/badge.svg)](https://github.com/RedFoxFinn/ChatList/actions/workflows/lint.yml)
![](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/RedFoxFinn/ChatList/main/docs/pylint_scores.json&label=Rating&query=score&color=informational)
![](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/RedFoxFinn/ChatList/main/docs/pylint_scores.json&label=Difference&query=diff&color=informational)

Verkkosovellus keskusteluryhmien listaamiseen ja niiden liittymislinkkien säilytykseen

Sovellus on toteutettu Helsingin Yliopiston kurssilla [Aineopintojen harjoitustyö: Tietokantasovellus (tsoha)](https://studies.helsinki.fi/opintotarjonta/cur/hy-opt-cur-2223-2e32cd2f-c204-4e8d-8233-b652d7194713)

## Sovelluksesta

Sovelluksen käyttötarkoitus: keskusteluryhmien sekä niiden liittymislinkkien ja ylläpitäjien listaaminen.

Ensisijaisesti kohdennettu telegram-ryhmille, mutta toteutettavissa myös muiden palveluiden keskusteluiden listaamiseen.

### Sovelluksen käynnistäminen

1:

Sovelluksen lähdekoodi ladataan omalle tietokoneelle lataamalla se GitHub-repositoriosta pakattuna yhdeksi arkistoksi, joka puretaan haluttuun hakemistoon.

Vaihtoehtoisesti lataamisen voi tehdä komennolla `git clone https://github.com/RedFoxFinn/ChatList.git` haluamaasi hakemistoon.


2:

Sovelluksen riippuvuudet asennetaan käyttämällä python3:n paketinhallintaa, pip3:a komentorivillä.

Mikäli python3 ei ole tietokoneellasi asennettuna, täytyy se asentaa ennen tämän vaiheen suorittamista.

Luodaan ensin python3:n virtuaaliympäristö:

  `python3 -m venv venv`

ja käynnistetään se:

  `source venv/bin/activate`

Tämän virtuaalisen ympäristön voi sulkea komennolla

  `deactivate`

Virtuaaliympäristön ollessa aktiivisena (esimerkiksi riippuvuuksien asennuksen aikana) alkaa komentorivillä komentokehoite (rivi, jolle komennot kirjoitetaan) merkinnällä `(venv)`.

Riippuvuuksien asentaminen tapahtuu komennolla

  `pip3 install -r requirements.txt`

Tämän komennon suorittamisessa voi mennä pieni hetki, kun paketinhallinta asentaa tarvittavat paketit ja pakettiversiot.

3:

Kun komento on suoritettu loppuun, määritetään sovelluksen ympäristömuuttujat uuteen tiedostoon, jonka nimeksi määritetään `.env` (piste alkuun).

Tuohon tiedostoon kirjoitetaan ensimmäiselle riville `DATABASE_URL=postgresql+psycopg2:///`, jonka perään ilman väliä tai muita merkkejä kirjoitetaan oma käyttäjätunnus (löytyy komentokehoitteen riviltä `(venv)` jälkeen ja ennen `@`-merkkiä)

Toiselle riville kirjoitetaan `USER_REGISTRATION_CODE=`, jonka perään kirjoitetaan haluttu merkkijono. Tämä merkkijono vaaditaan sovellukseen rekisteröidyttäessä ja ensimmäisen rekisteröityjän tunnuksesta tulee automaattisesti ylläpitäjä sovellukseen erityisillä oikeuksilla (superuser).

Kolmannelle riville kirjoitetaan `SECRET_KEY=`, jonka perään kirjoitetaan tai liitetään haluttu merkkijono. Tämä merkkijono toimii sovelluksen istuntotoimintojen avaimena ja ilman sitä, ei toiminto toimi lainkaan.

Neljännelle riville voi halutessaan syöttää vapaavalintaisen nimen, joka tulee sovelluksen käyttöliittymässä näytettäväksi nimeksi. Tämä on hyvä keino yksilöidä sovellus tietylle käyttäjäryhmälle, kuten harrasteporukalle. Kirjoita tällöin `CUSTOM_APP_NAME=` ja haluamasi nimi sovellukselle. Mikäli merkkijono on tyhjä tai se puuttuu, tulee sovelluksen nimeksi oletusarvoinen `ChatList`.

Viimeisenä `.env`-tiedostoon lisätään salasanan nollaustoimintoa varten rivi `PW_RESET_PLACEHOLDER_VALUE=`, jonka perään kirjoitetaan omavalintainen merkkijono. Tämä arvo syötetään käyttäjän salatun salasanan tilalle, jos käyttäjä on pyytänyt pääkäyttäjää nollaamaan salasanansa.
Kirjautuessaan uusiksi sovellukseen käyttäjä syöttää salasanakenttään merkkijonoksi `RESET_MY_PASSWORD`, jolloin hänet ohjataan uuden salasanan luontiin.

4:

Lopuksi ennen käynnistämistä virtuaaliympäristössä määritetään vielä sovelluksen tietokannan rakenne ja tarvittavat taulut komennolla

  `psql < schema.sql`

5:

Nyt kaikki on valmista ja sovellus voidaan käynnistää komennolla

  `flask run`

Sovellus toimii nyt tietokoneella, oletuksena verkkoselaimen osoitteessa `http://localhost:5000/`

### Sovelluksen käyttäminen

Kun sovellus otetaan käyttöön ja sillä ei ole vielä määritettyjä käyttäjiä, ohjautuu se ensimmäiseksi osoitteeseen `http://localhost:5000/init_site`.

![Sovelluksen käyttöönottoruutu](/docs/init_required.png)

Klikkaamalla painiketta 'Aloita määritys' sovellus ohjautuu käyttäjä rekisteröitymissivulle `http://localhost:5000/register`.

![Sovelluksen rekisteröitymisruutu](/docs/registration.png)

Ensimmäisenä rekisteröityvästä käyttäjästä tulee automaattisesti pääkäyttäjä (Admin), jolla on lisäksi superuser-status. Tämä status vaaditaan mm. ylläpitäjien muokkaukseen ja muokkauspyyntöjen hyväksyntään.

Rekisteröitymisen jälkeen näytetään viesti rekisteröitymisen onnistumisesta ja käyttäjä ohjataan kirjautumissivulle `http://localhost:5000/login`.

![Sovelluksen kirjautumisruutu](/docs/login.png)

Kirjautumisen onnistumisesta näytetään käyttäjälle viesti ja hänet ohjataan etusivulle.

![Sovelluksen etusivu](/docs/frontpage.png)

Pääkäyttäjille sovelluksessa on mahdollisuus käyttää hallintatyökaluja, joihin kuuluvat ryhmien (toimialueen kaltainen ominaisuus), keskusteluryhmien ja ylläpitäjien hallinta.

![Sovelluksen hallintanäkymän navigointi](/docs/management.png)

Ryhmien hallinnassa pääkäyttäjät voivat luoda uusia ryhmiä tai siirtyä muokkaamaan olemassaolevan ryhmän ominaisuuksia (nimi, rajoitustaso).

Keskusteluryhmien hallinnassa käyttäjä pystyy lisäämään keskusteluryhmiä. Lisääjästä tulee automaattisesti moderaattori keskustelulle.

Keskusteluryhmien listaus näytetään myös näkymässä, mutta etusivusta poiketen laajemmilla tiedoilla ja mahdollisuudella siirtyä keskusteluryhmän tietojen muokkaukseen. Keskusteluryhmää voi muokata ainoastaan sille moderaattoriksi merkitty käyttäjä tai pääkäyttäjä(t).

Sovelluksessa on myös kaikille näkyvä osio, statistiikka. Se nimensä mukaisesti esittää tilastotietoja sovelluksesta.

![Sovelluksen tilastotietonäkymä](/docs/statistics.png)

Kaikille eivät samat tiedot näy, esimerkiksi kirjautumattomille näytetään vain keskusteluryhmien kokonaismäärä ja aiheiden kokonaismäärä.

Sovelluksessa on lisäksi näkymä salasanan vaihtamiseen.
### Tietokanta

Sovellus käyttää PostgreSQL-tietokantaa tiedon pysyväissäilytykseen.

<details><summary>Tietokannassa käytettävät taulut</summary>
<p>

#### Users

sovelluksen käyttäjät sisältävä tietokantataulu

- id SERIAL PRIMARY KEY
- uname TEXT NOT NULL UNIQUE, käyttäjänimi
- pw_hash TEXT, käyttäjän salasana (kryptattuna),
- dm_link TEXT NOT NULL UNIQUE, linkki käyttäjän yksityisviestikeskusteluun

#### Admins

sovelluksen ylläpitäjät sisältävä tietokantataulu

pitää listaa sovelluksen käyttäjistä, joilla on ylläpitäjän oikeudet

- id SERIAL PRIMARY KEY
- user_id INTEGER NOT NULL REFERENCES Users (id)

#### Groups

sovelluksen ryhmät sisältävä tietokantataulu

ryhmällä tarkoitetaan joukkoa keskusteluryhmiä, joilla on yhteisiä ominaisuuksia

- id SERIAL PRIMARY KEY
- gname TEXT NOT NULL UNIQUE, ryhmän nimi
- restriction TEXT NOT NULL DEFAULT "NONE"
  - "NONE" osoittaa kyseisen ryhmän olevan julkisesti näytettävä
  - "LOGIN" osoittaa kyseisen ryhmän olevan kirjautumisen jälkeen näytettävä
  - "AGE" osoittaa kyseisen ryhmän olevan ikärajallinen, tällöin sen linkki näytetään vain ylläpitäjille
  - "SEC" osoittaa kyseisen ryhmän olevan rajoitettu, tällöin se näytetään listassa vain ylläpitäjille
- admin_id INTEGER NOT NULL REFERENCES Admins (id), kyseisen ryhmän merkitty ylläpitäjä

#### Topics

sovelluksen keskusteluryhmien aiheet sisältävä tietokantataulu

- id SERIAL PRIMARY KEY
- topic TEXT NOT NULL UNIQUE

#### Chats

sovelluksen keskusteluryhmät sisältävä tietokantataulu

- id SERIAL PRIMARY KEY
- cname TEXT NOT NULL
- topic_id INTEGER REFERENCES Topics (id)
- group_id INTEGER REFERENCES Groups (id)
- link TEXT NOT NULL
- moderator_id INTEGER REFERENCES Users (id), viittaukset käyttäjiin

#### Records

sovelluksen lokien säilytykseen osoitettu tietokantataulu (toiminnallisuus rakenteilla)

- id SERIAL PRIMARY KEY
- action TEXT NOT NULL, tapahtuman kuvaus
- user_id INTEGER NOT NULL REFERENCES Users (id), tapahtuman suorittaneen käyttäjän id
- action_time TIMESTAMP NOT NULL, tapahtuman aikaleima

</p>
</details>

### Toimintakuvaus

Sovelluksen toiminta on suhteellisen yksinkertainen ulkopuolisesti, mutta pinnan alla varsin monimutkainen.

Front endin eli käyttäjälle näkyvän osan toiminnot voidaan listata seuraavasti:

- listausnäkymä
  - julkinen versio
  - kirjautumista vaativa versio
    - kirjautumisrajoitetut keskustelut (näytetään listauksessa kirjautuneille)
    - ikärajoitetut keskustelut (näytetään listauksessa kirjautuneille, linkki näytetään ylläpitäjille)
    - rajoitetut keskustelut (näytetään listauksessa vain ylläpitäjille)
- kirjautumisnäkymä
- hallintanäkymä
  - keskusteluryhmän lisäys
  - keskusteluryhmän linkin päivittäminen (moderaattori/admin)
  - keskusteluryhmän nimen päivittäminen (moderaattori/admin)
  - keskusteluryhmän ryhmän vaihtaminen (moderaattori/admin)
  - keskusteluryhmän poistaminen (moderaattori/admin)
  - ryhmän lisääminen (admin)
  - ryhmän poistaminen (admin)
  - ylläpitäjästatuksien muuttaminen (admin)
  - sovelluksen tilastotiedot
- salasanan vaihtamisen näkymä

#### Listausnäkymä

Listausnäkymässä esitetään listamuodossa sovellukseen talletettuja keskusteluryhmiä ja niiden tietoja.

Listauksen esittämisessä käytetään rajoitustasoja, jotka vaikuttavat näytettävän tiedon määrään ja tarkkuuteen.

Listauksessa korostetaan mahdollista keskusteluryhmän rajoitustasoa kirjautuneiden listausnäkymässä.

##### Rajoitustaso "NONE"

Ei rajoituksia, tiedot esitetään julkisena.

##### Rajoitustaso "LOGIN"

Nimensä mukaisesti tason rajoitus perustuu käyttäjän kirjautumiseen ja ilman kirjautumista tämän tason rajoituksella merkittyä keskustelua ei esitetä listassa.

##### Rajoitustaso "AGE"

Rajoitustason tiedot esitetään kirjautuneelle käyttäjälle, mutta keskusteluryhmän linkkiä ei esitetä ilman ylläpitäjä-statusta.

##### Rajoitustaso "SEC"

Rajoitustason tiedot eivät tavalliselle käyttäjälle näy kirjautuneenakaan. Ylläpitäjille tiedot näkyvät listauksessa.

#### Kirjautumisnäkymä

Sovelluksella on kirjautumisnäkymä, jossa käyttäjä syöttää tunnuksensa ja salasanansa päästäkseen käyttämään rajoitetumpaa versiota palvelusta.

#### Salasanan vaihtamisen näkymä

Kirjautumistiedoista salasanan vaihtaminen on olennainen toiminnallisuus ja se on toteutettuna sovelluksessa.

#### Salasanan asettamisnäkymä

Uuden salasanan asettamisen näkymä salasanan nollauksen jälkeisen kirjautumisen yhteydessä esitettäväksi.
#### Hallintanäkymä

Näkymästä käsin voidaan lisätä, päivittää ja poistaa keskusteluryhmiä, lisätä ja poistaa ryhmiä sekä muuttaa ylläpitäjästatuksia.

#### Statistiikkanäkymä

Näkymässä esitetään kirjautuneille tilastotietoa sovelluksesta. Tietojen määrä ja tarkkuus riippuu osittain käyttäjän statuksesta l. onko tämä käyttäjä vai pääkäyttäjä.

## Teknologiat

Sovelluksen lähdekoodissa on käytetty pythonin versiota 3 ja se ei siten ole yhteensopiva pythonin versioiden 1 ja 2 kanssa. Suosittelemme käyttämään viimeisintä versiota ja pitämään päivitykset ajantasaisina.

### Python-kirjastot

Sovelluksen lähdekoodissa on lisäksi käytetty kirjastoja, joilla on toteutettu mm. sovelluksen palvelintoiminnallisuudet.

<details><summary>Käytetyt kirjastot</summary>
<p>

Ympäristömuuttujat
- python-dotenv

Palvelintoiminnot
- flask

Tietokantatoiminnot
- flask-sqlalchemy
- sqlalchemy
- psycopg2

Tietoturva
- Werkzeug (salasanojen kryptaus/dekryptaus)

Verkkosivut
- jinja2

</p>
</details>

## Muuta

[Kuvake sovellukselle](https://pixabay.com/vectors/chat-icon-symbol-business-2013193/)

[Kuvakkeen konversio favicon.ico-muotoon](https://favicon.io/favicon-converter/)

[Ikoneita UI:ssa](https://icon-sets.iconify.design/bi/)
