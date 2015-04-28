# -*- coding: utf-8 -*-
import time
import tester
from unidecode import unidecode 

def tcs(question):
    return tester.test_chatscript(question, 'testagent', 'localhost:1024', bot='Dent')

TIMEOUT = 1 #sec

def repeat_until(question, options):
    occurrences = []
    start = time.time()
    while len(occurrences) != len(options):
        res = tcs(question)
        if res not in occurrences:
            occurrences.append(res)
        # timeout
        if (time.time() - start) > TIMEOUT:
            return occurrences
    return occurrences

def assert_list(L1, L2):
    return len(L1) == len(L2) and sorted(L1) == sorted(L2)


class TestQAFeature(object):

    def test_server_is_launched(self):
        assert tcs('que es java')

    def test_que_es_java(self):
        assert u'sendSolr definition java' in tcs('que es java')

    def test_que_es_for(self):
        assert u'sendSolr definition for' in tcs('que es for')
        assert u'sendSolr definition for' in tcs('que es for?')

    def test_que_es_something_for(self):
        assert u'sendSolr definition for' in tcs('que es un for') 
        assert u'sendSolr definition for' in tcs('que es un for?')
        assert u'sendSolr definition for' in tcs('que es un bucle for')
        assert u'sendSolr definition for' in tcs('que es un bucle for?')

    def test_que_sabes_de_for(self):
        assert u'sendSolr definition for' in tcs('que sabes del for')
        assert u'sendSolr definition for' in tcs('que sabes sobre for')
        assert u'sendSolr definition for' in tcs('que sabes de un for')
        assert u'sendSolr definition for' in tcs('dime que sabes del for')
        assert u'sendSolr definition for' in tcs('dime lo que sepas sobre for')
        #assert u'sendSolr definition for' in tcs('quiza sepas algo del for') 
        #assert u'sendSolr definition for' in tcs('sabes algo acerca del for')


class TestSocialDialog(object):
    
    def test_server_is_launched(self):
        assert tcs('hola')

    def test_hola(self):
        question = u'hola'
        options = [u"Hola, soy Duke y estoy aqui para ayudarte.", u"Hola, ¿necesitas ayuda?", u"¡Hola!"]
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    def test_que_tal(self):
        question = u'que tal'
        options = [u"Hola, soy Duke y estoy aqui para ayudarte.", u"Hola, ¿necesitas ayuda?", u"¡Hola!"]
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    def test_eres_el_profesor(self): 
        question = u'eres el profesor'
        options = [u"No, soy un bot asistente para ayudarte a encontrar respuestas."]
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    def test_eres_un_profesor(self): 
        question = u'eres un profesor'
        options = [u"No, soy un bot asistente para ayudarte a encontrar respuestas."]
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    def test_quien_eres(self):
        question = u'quien eres'
        options = [u"Me llamo Duke y soy un bot asistente para ayudarte con tus preguntas."]
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    # def test_sabes_hacer(self):
    #     questions = [u'que sabes hacer', u'que pues hacer', u'muestrame que sabes hacer', u'dime que puesdes hacer']
    #     options = [u'Mi funcion es ayudarte a encontrar respuestas', u'Busco informacion en mis documentos de Java', u'¡Cualquier cosa!...nah, es broma, soy experto en Java']
    #     for question in questions:
    #         assert tcs(question) in options
    #         assert_list( repeat_until(question, options), options)

    def test_que_sabes_hacer(self):
        question = u'que sabes hacer?'
        options = [u"Mi funcion es ayudarte a encontrar respuestas", u"Busco información en mis documentos de Java", u'¡Cualquier cosa!...nah, es broma, soy experto en Java']
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    def test_y_tu_que_haces(self):
        question = u'y tu que haces?'
        options = [u"Mi funcion es ayudarte a encontrar respuestas", u"Busco información en mis documentos de Java", u'¡Cualquier cosa!...nah, es broma, soy experto en Java']
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    def test_bueno_dias(self):
        question = u'buenos dias'
        options = [u"Hola, buenos días", u"Buenos días"]
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    def test_adios(self):
        questions = [u'adios', u'ciao', u'agur', u'bye', u'bye bye']
        options = [u"¡Que tengas buen día!", u"Adiós ¡Gracias!"]
        for question in questions:
            assert tcs(question) in options
            assert_list( repeat_until(question, options), options)
    
    def test_adios_more_comples(self):
        questions = [u'bueno pues adios', u'ciao ciao', u'bueno bye bye']
        options = [u"¡Que tengas buen día!", u"Adiós ¡Gracias!"]
        for question in questions:
            assert tcs(question) in options
            assert_list( repeat_until(question, options), options)

    def test_hasta_otra(self):
        questions = [u'hasta otra', u'hasta luego', u'venga hasta otra']
        options = [u'Hasta luego, vuelve cuando quieras']
        for question in questions:
            assert tcs(question) in options
            assert_list( repeat_until(question, options), options)

    def test_muy_bien(self):
        question = u'muy bien'
        options = [u"Me alegro", u"Estupendo"]
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)

    def test_que_tengas_un_buen_dia(self):
        assert unidecode(tcs('que tengas un buen dia')) == unidecode(u'Tú también, ¡gracias!')

    def test_quien_eres(self):
        pass

    def test_que_es_un_bot(self):
        assert tcs(u'que es un bot asistente') == u"Un bot asistente es como un diccionario parlante, te contesta preguntas si las sabe"
        assert tcs(u'preguntas sobre que') == u"En mi caso sobre Java"
        assert tcs(u'solo eso') == u'Me gustaria aprender más'        
        # iter 2
        assert tcs(u'que es un bot') == u'Un bot es como un diccionario parlante, te contesta preguntas si las sabe'
        assert tcs(u'que preguntas') == u"En mi caso sobre Java"
        # iter 2
        assert tcs(u'que es un bot') == u'Un bot es como un diccionario parlante, te contesta preguntas si las sabe'
        assert tcs(u'cualquier tipo de preguntas') == u"En mi caso sobre Java"

    def test_insulto_feo(self):
        questions = [u'feo', u'eres fea', u'tu interfaz es horrenda', u'quita bicho']
        options = [u'Pues mi madre dice que soy muy guapo', u'8 de cada 10 usuarios consideran que tengo una interfaz muy agradable', u'Prefiero mi interfaz actual a una simple línea de comandos.', u'Tan poco estoy tan mal para ser una mascota']
        for question in questions:
            assert tcs(question) in options
            assert_list( repeat_until(question, options), options)

    def n(self):
        questions = [u'']
        options = [u'']
        for question in questions:
            assert tcs(question) in options
            assert_list( repeat_until(question, options), options)

    def one(self):
        question = u''
        options = [u""]
        assert tcs(question) in options
        assert_list( repeat_until(question, options), options)