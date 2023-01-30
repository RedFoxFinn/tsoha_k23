# ChatList

Verkkosovellus keskusteluryhmien listaamiseen ja niiden liittymislinkkien säilytykseen

Sovellus on toteutettu Helsingin Yliopiston kurssilla [Aineopintojen harjoitustyö: Tietokantasovellus (tsoha)](https://studies.helsinki.fi/opintotarjonta/cur/hy-opt-cur-2223-2e32cd2f-c204-4e8d-8233-b652d7194713)

## Sovelluksesta

Sovelluksen käyttötarkoitus: keskusteluryhmien sekä niiden liittymislinkkien ja ylläpitäjien listaaminen.

Ensisijaisesti kohdennettu telegram-ryhmille, mutta toteutettavissa myös muiden palveluiden keskusteluiden listaamiseen.

### Tietokanta

Sovellus käyttää PostgreSQL-tietokantaa tiedon pysyväissäilytykseen.

<details><summary>Tietokannassa käytettävät taulut</summary>
<p>

#### Users

sovelluksen käyttäjät sisältävä tietokantataulu

- id SERIAL PRIMARY KEY
- uname TEXT NOT NULL UNIQUE, käyttäjänimi
- pw_hash TEXT, käyttäjän salasana (kryptattuna)

#### Admins

sovelluksen ylläpitäjät sisältävä tietokantataulu

pitää listaa sovelluksen käyttäjistä, joilla on ylläpitäjän oikeudet

- id SERIAL PRIMARY KEY
- user_id INTEGER NOT NULL REFERENCES Users (id)
- superuser BOOLEAN DEFAULT FALSE

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
- moderator_ids INTEGER[], viittaukset keskusteluryhmän ylläpitäjiin

#### Moderators

sovelluksen keskusteluryhmien ylläpitäjät sisältävä tietokantataulu

- id SERIAL PRIMARY KEY
- handle TEXT NOT NULL UNIQUE
- chat_link TEXT NOT NULL

#### Requests

sovelluksen tietoihin kohdistuvien muutosten hyväksymispyynnöt sisältävä tietokantataulu

- id SERIAL PRIMARY KEY
- user_id INTEGER NOT NULL REFERENCES Users (id), muutoksen pyytänyt käyttäjä
- info_table TEXT NOT NULL, taulu, jonka tietoa pyydetään muutettavan
- info_id INTEGER NOT NULL, taulun rivi, jota pyydetään muutettavan
- change_type TEXT NOT NULL, muutostyyppi (DELETE/UPDATE)
- change_info TEXT[], muutokset

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
- hallintanäkymä (ylläpitäjät)
  - keskusteluryhmän lisäys
  - keskusteluryhmän linkin päivittäminen
  - keskusteluryhmän nimen päivittäminen
  - keskusteluryhmän ryhmän vaihtaminen (superuser TRUE -admin tai erillinen hyväksyntä em. adminilta)
  - keskusteluryhmän ylläpitäjien päivittäminen
  - keskusteluryhmän poistaminen (superuser TRUE -admin tai erillinen hyväksyntä em. adminilta)
  - ryhmän lisääminen
  - ryhmän poistaminen (superuser TRUE -admin tai erillinen hyväksyntä em. adminilta)
  - ylläpitäjästatuksien muuttaminen (superuser TRUE -admin)
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

#### Hallintanäkymä

Hallintanäkymä ylläpitäjille. Näkymästä käsin voidaan lisätä, päivittää ja poistaa keskusteluryhmiä, lisätä ja poistaa ryhmiä sekä muuttaa ylläpitäjästatuksia. Näkymässä on esitettynä myös sovelluksen tilastotietoja.

## Teknologiat

Sovelluksen lähdekoodissa on käytetty pythonin versiota 3 ja se ei siten ole yhteensopiva pythonin versioiden 1 ja 2 kanssa. Suosittelemme käyttämään viimeisintä versiota ja pitämään päivitykset ajantasaisina.

### Python-kirjastot

Sovelluksen lähdekoodissa on lisäksi käytetty kirjastoja, joilla on toteutettu mm. sovelluksen palvelintoiminnallisuudet.

<details><summary>Käytetyt kirjastot</summary>
<p>

Ympäristömuuttujat
- dotenv
- python-dotenv

Palvelintoiminnot
- flask

Tietokantatoiminnot
- flask-sqlalchemy
- sqlalchemy
- psycopg2

Tietoturva
- Werkzeug (salasanojen kryptaus/dekryptaus)

</p>
</details>

## Muuta

[Kuvake sovellukselle](https://pixabay.com/vectors/chat-icon-symbol-business-2013193/)

[Kuvakkeen konversio favicon.ico-muotoon](https://favicon.io/favicon-converter/)