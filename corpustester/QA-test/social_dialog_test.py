# -*- coding: utf-8 -*-
import itertools
import pytest
import time
import tester
from unidecode import unidecode 

def tcs(question, agent=None):
    if not agent:
        agent = 'testagent'
    return tester.test_chatscript(question, agent, 'localhost:1024', bot='Dent')

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
    
    @pytest.fixture(scope="session", autouse=True)
    def build_bot(self):
        tcs(':build Dent')

    def test_server_is_launched(self):
        assert tcs('hola')

    def test_hola(self):
        question = u'hola'
        options = [u"Hola, soy Duke y estoy aqui para ayudarte.", u"Hola, ¿necesitas ayuda?", u"¡Hola!", u"Entra, <i>Mellon</i>, y pregunta."]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_que_tal(self):
        question = u'que tal'
        options = [u"Hola, soy Duke y estoy aqui para ayudarte.", u"Hola, ¿necesitas ayuda?", u"¡Hola!", u"Entra, <i>Mellon</i>, y pregunta."]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_eres_el_profesor(self): 
        question = u'eres el profesor'
        options = [u"No, soy un bot asistente para ayudarte a encontrar respuestas.", u"Ya me gustaría. Solo soy un bot que responde preguntas de java.", u"Por supuesto. ¡Estás suspenso! Na, es broma. Soy un bot inteligente."]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_eres_un_profesor(self): 
        question = u'eres un profesor'
        options = [u"No, soy un bot asistente para ayudarte a encontrar respuestas.", u"Ya me gustaría. Solo soy un bot que responde preguntas de java.", u"Por supuesto. ¡Estás suspenso! Na, es broma. Soy un bot inteligente."]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_quien_eres(self):
        question = u'quien eres'
        options = [u"Me llamo Duke y soy un bot asistente para ayudarte con tus preguntas.", u"Duke, encantado de conocerte. Soy un bot especializado en java", u"Duke en mi nombre. Responder tus dudas yo debo"]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_sabes_hacer(self):
        questions = [u'que sabes hacer', u'que pues hacer', u'muestrame que sabes hacer', u'dime que puesdes hacer']
        options = [u"Mi función es ayudarte a encontrar respuestas", u"Lo mío es buscar información sobre java y ayudarte con tus dudas", u"Un bot Duke es. ¡Cosas sobre java que explicarte tengo!", u"Busco información en mis documentos de Java", u'¡Cualquier cosa!...nah, es broma, soy experto en Java']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)

    def test_que_sabes_hacer(self):
        question = u'que sabes hacer?'
        options = [u"Mi función es ayudarte a encontrar respuestas", u"Lo mío es buscar información sobre java y ayudarte con tus dudas", u"Un bot Duke es. ¡Cosas sobre java que explicarte tengo!", u"Busco información en mis documentos de Java", u'¡Cualquier cosa!...nah, es broma, soy experto en Java']
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_y_tu_que_haces(self):
        question = u'y tu que haces?'
        options = [u"Mi función es ayudarte a encontrar respuestas", u"Lo mío es buscar información sobre java y ayudarte con tus dudas", u"Un bot Duke es. ¡Cosas sobre java que explicarte tengo!", u"Busco información en mis documentos de Java", u'¡Cualquier cosa!...nah, es broma, soy experto en Java']
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_bueno_dias(self):
        question = u'buenos dias'
        options = [u"Hola, buenos días", u"Buenos días"]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_adios(self):
        questions = [u'adios', u'ciao', u'agur', u'bye', u'bye bye']
        options = [u"¡Que tengas buen día!", u"Adiós ¡Gracias!"]
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)
    
    def test_adios_more_complex(self):
        questions = [u'bueno pues adios', u'ciao ciao', u'bueno bye bye']
        options = [u"¡Que tengas buen día!", u"Adiós ¡Gracias!"]
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)

    def test_hasta_otra(self):
        questions = [u'hasta otra', u'hasta luego', u'venga hasta otra']
        options = [u'Hasta luego, vuelve cuando quieras']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)

    def test_muy_bien(self):
        question = u'muy bien'
        options = [u"Me alegro", u"Estupendo"]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_que_tengas_un_buen_dia(self):
        assert unidecode(tcs('que tengas un buen dia')) == unidecode(u'Tú también, ¡gracias!')

    def test_llegas_tarde(self):
        question = u'llegas tarde'
        options = [u"Un bot nunca llega tarde, está siempre dispuesto a ayudar con sus respuestas", u"Ya, bueno. No soy un mago de barba gris, que le voy a hacer."]
        assert tcs(question) in options

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
            assert assert_list( repeat_until(question, options), options)

    def test_insulto_tonto(self):
        questions = [u'eres tonto', u'tonta', u'serás boba', u'qué estupido eres']
        options = [u'Lo siento, a veces me cuesta entender las cosas, pero intento hacerlo lo mejor que puedo.', u'Aunque sea un bot me duele que me digan esas cosas...', u'Para ser sólo unos y ceros creo que no me desenvuelvo mal...', u'Mi autoestima disminuye con esos calificativos...', u'Aunque a veces no entienda lo que me dice me esfuerzo mucho por ayudarte...']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)

    def test_mala_educacion(self):
        questions = [u'me cago en todo', u'que te den por culo', u'joder']
        options = [u'Vaya lenguaje...', u'Se pueden decir las cosas de manera educada...', u'No me gusta ese lenguaje']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)

    def test_insulto_fuerte(self):
        questions = [u'anormal', u'cabron', u'gilipollas']
        options = [u'Sin insultar, por favor.', u'No hace falta decir tacos...', u'No deberías ser tan maleducad@.']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)    

    def test_insulto_ingenioso(self):
        question = u'Zopenco'
        options = [u'Jeje, que gracia', u'Jeje']
        assert tcs(question) in options
        
    def test_insulto_segunda_interaccion(self):
        questions = [u'Zopenco', u'Bocachancla', u'si']
        options = [[u'Jeje, que gracia', u'Jeje'], [u'Estamos graciosos, ¿no?', u'Estamos de buen humor, ¿no?'], [u'Eso es bueno', u'Me alegro'] ]
        for _ in itertools.repeat(None, 10):
            for index, question in enumerate(questions):
                assert tcs(question, agent="asd") in options[index]

    def n(self):
        questions = [u'']
        options = [u'']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)

    def one(self):
        question = u''
        options = [u""]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def seq(self):
        questions = [u'', u'']
        options = [[u'', u''], [u'', u''] ]
        for _ in itertools.repeat(None, 10):
            for index, question in enumerate(questions):
                assert tcs(question) in options[index]