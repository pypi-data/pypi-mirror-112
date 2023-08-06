"""Define the litcorpt data models"""
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods

from enum import Enum
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, ValidationError


##############################################################
# Enumeration classes
##############################################################
class CreatorRolesEnum(str, Enum):
    """Enumeration for Creator Roles"""
    AUTHOR: str = 'author'
    EDITOR: str = 'editor'
    TRANSLATOR: str = 'translator'
    ORGANIZER: str = 'organizer'


class OrtographyEnum(str, Enum):
    """Enumeration for Ortographic Agreements
       https://pt.wikipedia.org/wiki/Ortografia_da_l%C3%ADngua_portuguesa
    """
    FN1200: str = '1200fonetico'
    ET1500: str = '1500etimologico'
    PT1885: str = '1885portugal'
    BR1907: str = '1907brasil'
    PT1911: str = '1911portugal'
    BR1915: str = '1915brasil'
    LS1931: str = '1931lusofono'
    BR1943: str = '1943brasil'
    LS1945: str = '1945lusofono'
    BR1971: str = '1971brasil'
    PT1973: str = '1973portugal'
    LS1975: str = '1975lusofono'
    BR1986: str = '1986brasil'
    LS1990: str = '1990lusofono'

class LicenseEnum(str, Enum):
    """License Enumeration"""
    PUBLIC: str = 'Public Domain'
    PRIVATE: str = 'Copyrighted'
    CC: str = 'Creative Commons'
    ACADEMIC: str = 'Free for academic usage'
    SPECIAL: str = 'Special use'
    UNKNOWN: str = 'Unknown'


##############################################################
# Model classes
##############################################################
class Creator(BaseModel):
    """Define creator elements"""
    role: CreatorRolesEnum
    lastname: Optional[str]
    firstname: Optional[str]
    birth: Optional[int]
    death: Optional[int]
    place: Optional[str]


class Book(BaseModel):
    """Book entry model

    This class define the elements of a book entry.

    index:             An unique string to internaly identify the entry.
    title:             A list of titles associated to the entry. Often is
                       a list with a single element.
    creator:           A list of creators. Each creator contains:
                           Role: Creator relationship with the book entry
                           LastName: creator last name, often used in bibliography,
                           FirstName: creator given name,
                           Birth: Creator's birth year.
                           Death: Creator's death year.
                           Place: Creator's birth place.
    language:          A list of ISO entry with language, pt_BR or pt are the
                       most common here.  A document can contain many languages.
                       Most of time just one.
    published:         Date of first publish. Multiple edition should use the
                       date of first edition. Except when large changes happened
                       in document, as change of translator, change of ortography.
    identifier:        A unique global identifier, often a ISBN13 for books.
    original_language: Original language of document. Using ISO entry for language.
    subject:           A list entry subjects. As example: Fantasy, Science-Fiction, Kids.
                       Use lower caps always.
    genre:             A list of literary genre: Novel, Poetry, Lyrics, Theather.
                       Use lower caps always.
    ortography:        Reference to which Portuguese ortography is being used.
    abstract:          The book abstract/resume.
    notes:             Any notes worth of note.
    contents:          Book contents. The text itself.

    Caution: Date fields must contain a datetime.date or a string in format "YYYY-MM-DD"
    """

    index: str
    title: List[str]
    creator: List[Creator]
    language: List[str]
    published: Optional[date]
    identifier: Optional[List[str]]
    original_language: Optional[List[str]]
    subject: Optional[List[str]]
    genre: Optional[List[str]]
    ortography: Optional[OrtographyEnum]
    abstract: Optional[str]
    notes: Optional[List[str]]
    license: Optional[LicenseEnum] = LicenseEnum.UNKNOWN
    contents: Optional[str]

    # @validator('subject')
    # def validate_list_lower_subject(cls, field: Optional[str]) -> None:
    #     """Every entry must be in lower case"""
    #     if field is not None:
    #         for entry in field:
    #             if entry != entry.lower():
    #                 raise ValueError(f"""Entry '{entry}' must be lower case""")

    # @validator('genre')
    # def validate_list_lower_genre(cls, field: Optional[str]) -> None:
    #     """Every entry must be in lower case"""
    #     if field is not None:
    #         for entry in field:
    #             if entry != entry.lower():
    #                 raise ValueError(f"""Entry '{entry}' must be lower case""")


##############################################################
# Main test function
##############################################################
def test_book() -> Book:
    """Return a Book for testing purposes."""
    assis_memorias = {
        'index': 'assismemorias1880',
        'title': [ 'Memórias Póstumas de Brás Cubas', 'Epitáfio de um Pequeno Vencedor' ],
        'creator': [
            {'role': 'author',
             'lastname': 'Assis',
             'firstname': 'Machado de',
             'birth': '1839',
             'death': '1908',
            }
        ],
        'language': ['pt_BR'],
        'published': '1881-01-01',
        'original_language': ['pt_BR'],
        'subject': ['realism', 'humor'],
        'genre': ['novel', 'prose'],
        'ortography': '1990lusofono'
    }

    return Book(**assis_memorias)


#%%
def test_book_contents() -> str:
    """Return a book contents for testing"""
    memorias = """
                                        AO VERME
                                           QUE
                              PRIMEIRO ROEU AS FRIAS CARNES
                                      DO MEU CADÁVER
                                          DEDICO
                                  COMO SAUDOSA LEMBRANÇA
                                          ESTAS

                                    Memórias Póstumas



Prólogo da quarta edição


A PRIMEIRA edição destas Memórias póstumas de Brás Cubas foi feita aos
pedaços na Revista Brasileira, pelos anos de 1870. Postas mais tarde em
livro, corrigi o texto em vários logares. Agora que tive de o rever para
a terceira edição, emendei ainda alguma cousa e suprimi duas ou três
dúzias de linhas. Assim composto, sai novamente à luz esta obra que
alguma benevolência parece ter encontrado no público.
Capistrano de Abreu, noticiando a publicação do livro, perguntava:
« As Memórias Póstumas de Brás Cubas são um romance? » Macedo So-
ares, em carta que me escreveu por esse tempo, recordava amigamente
as Viagens na minha terra. Ao primeiro respondia já o defuncto Brás Cu-
bas (como o leitor viu e verá no prólogo dele que vai adeante) que sim
e que não, que era romance para uns e não o era para outros. Quanto
ao segundo, assim se explicou o finado: « Trata-se de uma obra difusa,
na qual eu, Brás Cubas, se adoptei a forma livre de um Sterne ou de
um Xavier de Maistre, não sei se lhe meti algumas rabugens de pessi-
mismo. » Toda essa gente viajou: Xavier de Maistre à roda do quarto,
Garrett na terra dele, Sterne na terra dos outros. De Brás Cubas se pode
talvez dizer que viajou à roda da vida.
O que faz do meu Brás Cubas um autor particular é o que ele chama
« rabugens de pessimismo » . Há na alma deste livro, por mais risonho
que pareça, um sentimento amargo e áspero, que está longe de vir dos
seus modelos. É taça que pode ter lavores de igual escola, mas leva outro
vinho. Não digo mais para não entrar na crítica de um defunto, que se
pintou a si e a outros, conforme lhe pareceu melhor e mais certo.

MACHADO DE A SSIS


Ao leitor

QUE STENDHAL confessasse haver escripto um de seus livros para cem
leitores, cousa é que admira e consterna. O que não admira, nem pro-
vavelmente consternará é se este outro livro não tiver os cem leitores de
Stendhal, nem cincoenta, nem vinte, e quando muito, dez. Dez? Talvez
cinco. Trata-se, na verdade, de uma obra difusa, na qual eu, Brás Cu-
bas, se adoptei a forma livre de um Sterne, ou de um Xavier de Maistre,
não sei se lhe meti algumas rabugens de pessimismo. Pode ser. Obra de
finado. Escrevi-a com a pena da galhofa e a tinta da melancolia, e não
é difícil antever o que poderá sair desse conúbio. Acresce que a gente
grave achará no livro umas aparências de puro romance, ao passo que a
gente frívola não achará nele o seu romance usual; ei-lo aí fica privado
da estima dos graves e do amor dos frívolos, que são as duas colunas
máximas da opinião.
Mas eu ainda espero angariar as simpatias da opinião, e o primeiro
remédio é fugir a um prólogo explícito e longo. O melhor prólogo é o que
contém menos cousas, ou o que as diz de um jeito obscuro e truncado.
Conseguintemente, evito contar o processo extraordinário que empre-
guei na composição destas Memórias, trabalhadas cá no outro mundo.
Seria curioso, mas nimiamente extenso, e aliás desnecessário ao enten-
dimento da obra. A obra em si mesma é tudo: se te agradar, fino leitor,
pago-me da tarefa; se te não agradar, pago-te com um piparote, e adeus.
BRÁS CUBAS


CAPÍTULO PRIMEIRO

Óbito do autor
ALGUM tempo hesitei se devia abrir estas memórias pelo princípio ou
pelo fim, isto é, se poria em primeiro logar o meu nascimento ou a
minha morte. Suposto o uso vulgar seja começar pelo nascimento, duas
considerações me levaram a adoptar diferente método: a primeira é que
eu não sou propriamente um autor defunto, mas um defunto autor, para
quem a campa foi outro berço; a segunda é que o escripto ficaria assim
mais galante e mais novo. Moisés, que também contou a sua morte, não
a pôs no intróito, mas no cabo: diferença radical entre este livro e o
Pentateuco.

Continua...
"""

    return memorias


def main() -> None:
    """Run basic tests for models"""
    try:
        assis_book = test_book()
    except ValidationError as err:
        print(f"Error in book: {err}")
    else:
        print(f"Python Object:\n {assis_book}\n")
        print(f"Json   Object:\n {assis_book.json()}\n")


if __name__ == "__main__":
    main()
