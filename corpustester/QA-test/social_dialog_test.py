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

def assert_list_exact(L1, L2):
    return len(L1) == len(L2) and sorted(L1) == sorted(L2)

def assert_list_fuzzy(L1, L2):
    if len(L1) != len(L2):
        return False
    sorted_l = sorted(L1)
    for index, item in enumerate(sorted(L2)):
        if item.lower() not in sorted_l[index].lower():
            return False
    return True

def assert_list(L1, L2):
    return assert_list_exact(L1, L2)


class TestQAFeature(object):

    def test_server_is_launched(self):
        assert tcs('que es java')

    def test_que_es_java(self):
        assert u'sendSolr definition java' in tcs(u'que es java?')

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


class TestBugsFromLogs (object):

    @pytest.fixture(scope="session", autouse=True)
    def build_bot(self):
        tcs(':build Dent reset')  
        tcs('hola')

    def test_que_es_un_set(self):
        assert u'sendSolr definition set' in tcs(u'que es un set?')

    def test_que_son_los_sets(self):
        assert u'sendSolr definition sets' in tcs(u'que son los sets?')

    def test_que_son_los_mapas(self):
        assert u'sendSolr definition mapas' in tcs(u'que son los mapas?')

    def test_que_es_un_mapa(self):
        assert u'sendSolr definition mapa' in tcs(u'que es un mapa?')

    def test_hola_ensename_que_es_un_while (self):
        assert u'sendSolr definition while' in tcs(u'hola, enseñame que es un while')

    def test_hola_que_es_un_metodo_estatico (self):
        assert u'sendSolr definition estatico' in tcs(u'Hola, que es un metodo estatico?')

    def test_ya_que_es_un_metodo_estatico (self):
        assert u'sendSolr definition estatico' in tcs(u'ya... que es un metodo estatico?')

    def test_gracias_por_todo(self):
        assert tcs(u'gracias por todo') in [u'De nada', u'De nada, ha sido un placer']

    def test_sabes_hablar(self):
        assert u'No, por ahora sólo puedo escribir' in tcs(u'sabes hablar?')

    def test_sabes_hablar_2iter(self):
        options1= [u'No, por ahora sólo puedo escribir']
        options2 = [u'Mi función es ayudarte a encontrar respuestas',
                   u'Lo mío es buscar información sobre java y ayudarte con tus dudas',
                   u'Un bot Duke es. ¡Cosas sobre java que explicarte tengo!',
                   u'Busco información en mis documentos de Java',
                   u'¡Cualquier cosa! ...nah, es broma, soy experto en Java']
        assert tcs(u'sabes hablar?') in options1
        assert tcs(u'sobre?') in options2
        assert tcs(u'sabes hablar?') in options1
        assert tcs(u'de que') in options2

    # def test_sabes_hablar_questionmark(self):
    #     assert u'No, por ahora sólo puedo escribir' in tcs(u'¿sabes hablar?')

    def test_eres_capaz_de_hablar(self):
        assert u'No, por ahora sólo puedo escribir' in tcs(u'eres capaz de hablar?')

    def test_sabes_comunicarte(self):
        assert tcs(u'sabes comunicarte?') in [u'Sí, ya sabes pregúntame sobre Java', u'Sí, ¿de qué quieres que hablemos?']

    def test_sabes_comunicarte_2iter(self):
        options1 = [u'Sí, ya sabes pregúntame sobre Java', u'Sí, ¿de qué quieres que hablemos?']
        assert tcs(u'sabes comunicarte?') in options1
        assert tcs(u'java') in u'¡Estupendo! Mi tema favorito'
        assert tcs(u'sabes comunicarte?') in options1
        assert tcs(u'de lo que quieras') in u'Bueno, yo preferiría hablar de Java que es lo que se me da bien'
        assert tcs(u'sabes comunicarte?') in options1
        assert tcs(u'de orange') in u'¿En serio? Conocía a una chicabot que sabía de esos temas, se llamaba Erika'
        assert tcs(u'y yo') in u'Qué coincidencia'

    def test_has_comido_hoy (self):
        assert u'Yo no como, soy un bot' in tcs(u'has comido hoy?')

    def test_vas_a_desayunar (self):
        assert u'Yo no como, soy un bot' in tcs(u'vas a desayunar?')

    def test_como_funcionan_los_comentarios (self):
        assert u'No se como funciona los comentarios' in tcs(u'como funcionan los comentarios?')
        assert u'Te puedo dar información teorica' in tcs(u'como funcionan los comentarios?')
        assert u'label comentarios' in tcs(u'como funcionan los comentarios?')
        assert u'sendSolr definition comentarios' in tcs(u'como funcionan los comentarios?')
        
    def test_como_funciona_el_while (self):
        assert u'No se como funciona el while' in tcs(u'como funciona el bucle while?')
        assert u'Te puedo dar información teorica' in tcs(u'como funciona el bucle while?')
        assert u'label while' in tcs(u'como funciona el bucle while?')
        assert u'sendSolr definition while' in tcs(u'como funciona el bucle while?')

    def test_como_construir_un_condicional (self):
        assert u'No se como funciona el while' in tcs(u'como construir el while?')
        assert u'No se como funciona el while' in tcs(u'como se construye el while?')


class TestIdeQuestions (object):

    @pytest.fixture(scope="session", autouse=True)
    def build_bot(self):
        tcs(':build Dent reset')  
        tcs('hola')

    # Que ser
    def test_que_es_netbeans (self):
        questions = [u'que es netbeans', u'que sabes de netbeans', u'explicame que es netbeans']
        options = [u'No sabría hablarte de las características exactas de netbeans, pero puedes consultar esta comparativa',
                   u'Es un IDE de Java, ¿no? En esta página salen más',
                   u'Para saber de netbeans, lo mejor será que mires esta comparativa de IDEs']
        for question in questions:
            assert assert_list_fuzzy( repeat_until(question, options), options)

    def test_que_es_intellij (self):
        questions = [u'que es intellij', u'que sabes de intellij', u'explicame que es intellij']
        options = [u'No sabría hablarte de las características exactas de intellij, pero puedes consultar esta comparativa',
                   u'Es un IDE de Java, ¿no? En esta página salen más',
                   u'Para saber de intellij, lo mejor será que mires esta comparativa de IDEs']
        for question in questions:
            res = tcs(question)
            assert assert_list_fuzzy( repeat_until(question, options), options)

    def test_que_idelist_resource (self):
        questions = [u'que es intellij', u'que es netbeans', u'que sabes de eclipse', u'que es NetBeans', u'que sabes de Eclipse', u'que es IntelliJ', u'que es Intellij']
        for question in questions:
            assert u'¬resource http://goo.gl/9gzJI7' in tcs(question)

    # Como funciona

    def test_saber_usar_eclipse (self):
        questions = [u'sabes utilizar eclipse', u'sabes trabajar con bluej', u'sabrías usar intellij']
        for question in questions:
            assert u'No sé utilizar ningún IDE en particular, a mi me gusta más la teoría' in tcs(question)

    def test_como_funciona_eclipse (self):
        questions = [u'como funciona eclipse', u'como configuro bluej', u'como funciona intellij']
        for question in questions:
            res = tcs(question)
            assert u'Para saber como funciona' in res
            assert u'lo mejor es irse al manual' in res
            assert u'¬resource http://www.google.es/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=manual%20' in res

    # Preferencias de uso
    def test_que_entorno_de_desarrollo_prefieres (self):
        questions = [u'que entorno de desarrollo prefieres', u'que entorno de desarrollo te parece mejor', u'que entorno de desarrollo es mejor']
        options = [u'Mis programadores no tienen preferencias, así que te muestro una comparativa para que decidas tú mismo', u'Yo no utilizo ningún entorno de desarrollo en particular, pero échale un ojo a esto para comparar']
        for question in questions:
            res = tcs(question)
            assert assert_list_fuzzy( repeat_until(question, options), options)

    def test_que_IDE_prefieres (self):
        questions = [u'que IDE prefieres', u'que IDE parece mejor', u'que IDE funciona mejor']
        options = [u'Mis programadores no tienen preferencias, así que te muestro una comparativa para que decidas tú mismo', u'Yo no utilizo ningún IDE en particular, pero échale un ojo a esto para comparar']
        for question in questions:
            res = tcs(question)
            assert assert_list_fuzzy( repeat_until(question, options), options)

    def test_que_entorno_de_desarrollo_prefieres_resource (self):
        questions = [u'que IDE prefieres', u'que herramienta de programación te parece mejor', u'que herramienta te parece mejor', u'que entorno para programar prefieres', u'que IDE debería usar', u'que entorno debo usar', u'en que herramienta prefieres para programar']
        for question in questions:
            assert u'¬resource http://goo.gl/9gzJI7' in tcs(question)

    def test_que_entorno_de_desarrollo_utilizas (self):
        questions = [u'que entorno de desarrollo utilizas', u'que entorno de desarrollo usas', u'en que entorno de desarrollo programas']
        options = [u'No sé utilizar ningún IDE en particular, a mi me gusta más la teoría']
        for question in questions:
            res = tcs(question)
            assert assert_list_fuzzy( repeat_until(question, options), options)

    def test_que_IDE_utilizas (self):
        questions = [u'que IDE utilizas', u'que IDE usas', u'en que IDE programas']
        options = [u'No sé utilizar ningún IDE en particular, a mi me gusta más la teoría']
        for question in questions:
            res = tcs(question)
            assert assert_list_fuzzy( repeat_until(question, options), options)

    # Fallback
    def test_te_suena_drjava(self):
        questions = [u'te suena eclipse', u'te suena drjava', u'netbeans']
        for question in questions:
            res = tcs(question)
            assert u'¿Te refieres al entorno de desarrollo? Lo mejor será que mires esta comparativa' in res
            assert u'¬resource http://goo.gl/9gzJI7' in res


class TestRejoinders(object):

    @pytest.fixture(scope="function", autouse=True)
    def build_bot(self):
        tcs(':build Dent reset')


    def test_rejoinder_order_without_questioning(self):
        assert tcs('unrecognised sentence') == u'¿Cómo estás?'
        assert tcs('unrecognised sentence') == u'¿En qué puedo ayudarte?'
        assert tcs('unrecognised sentence') == u'¿Sabías que me puedes preguntar por programación en Java?'
        assert tcs('unrecognised sentence') == u'No controlo todos los temas, pero de algunos sé bastante'
        assert tcs('unrecognised sentence') not in [u'¿Se te da bien la programación?', u'¿Te gusta Java?', u'¿Quieres responder a una encuesta? No te llevará ni 5 minutos']

    def test_rejoinder_order_questioning_first(self):
        tcs(u'Hola')
        tcs(u'que es Java?')
        assert tcs('cuantas preguntas') == u'Llevas 1 preguntas'
        assert tcs('unrecognised sentence') == u'¿En qué puedo ayudarte?'
        assert tcs('unrecognised sentence') == u'No controlo todos los temas, pero de algunos sé bastante'
        assert tcs('unrecognised sentence') == u'¿Se te da bien la programación?'
        assert tcs('unrecognised sentence') == u'¿Te gusta Java?'
        assert tcs('unrecognised sentence') != u'¿Quieres responder a una encuesta? No te llevará ni 5 minutos'

    def test_rejoinder_order_questioning_between(self):
        assert tcs('unrecognised sentence') == u'¿Cómo estás?'
        assert tcs('unrecognised sentence') == u'¿En qué puedo ayudarte?'        
        assert tcs('unrecognised sentence') == u'¿Sabías que me puedes preguntar por programación en Java?'
        assert tcs('unrecognised sentence') == u'No controlo todos los temas, pero de algunos sé bastante'
        tcs(u'que es java?')
        assert tcs('unrecognised sentence') == u'¿Se te da bien la programación?'
        assert tcs('unrecognised sentence') == u'¿Te gusta Java?'
        tcs(u'que es java?')
        tcs(u'que es java?')
        tcs(u'que es java?')
        assert tcs('unrecognised sentence') == u'¿Quieres responder a una encuesta? No te llevará ni 5 minutos'

class TestSocialDialog(object):
    
    @pytest.fixture(scope="session", autouse=True)
    def build_bot(self):
        tcs(':build Dent reset')

    def test_server_is_launched(self):
        assert tcs('hola')

    def test_estoy_negativo(self):
        questions = [u'estoy triste', u'porque no me gusta esto']
        options = [[u'¿Por qué estás triste?', u'¿Cómo es que estás triste?'], [u'Entiendo', u'Comprendo']]
        for _ in itertools.repeat(None, 10):
            for index, question in enumerate(questions):
                assert tcs(question, agent="estoynegativo") in options[index]
        #iter 2
        questions = [u'me encuentro cansado', u'me siento agotado', u'no sé']
        options = [[u'¿Por qué estás cansado?', u'¿Cómo es que estás cansado?'], [u'¿Por qué estás agotado?', u'¿Cómo es que estás agotado?'], [u'Oh']]
        for _ in itertools.repeat(None, 10):
            for index, question in enumerate(questions):
                assert tcs(question, agent="estoynegativo") in options[index]
        #iter 3
        questions = [u'me encuentro enfadada', u'me siento frustrada', u'no sé']
        options = [[u'¿Por qué estás enfadada?', u'¿Cómo es que estás enfadada?'], [u'¿Por qué estás frustrada?', u'¿Cómo es que estás frustrada?'], [u'Oh']]
        for _ in itertools.repeat(None, 10):
            for index, question in enumerate(questions):
                assert tcs(question, agent="estoynegativo") in options[index]

    def test_estoy_mal(self):
        questions = [u'estoy mal', u'no se']
        options = [[u'Vaya ¿qué te pasa?', u'Vaya ¿qué te ocurre?'], [u'Lo siento', u'Si pudiera hacer algo...']]
        for _ in itertools.repeat(None, 10):
            for index, question in enumerate(questions):
                assert tcs(question, agent="estoymal") in options[index]

    def test_estoy_positivo_different_verbs(self):
        questions = [u'Estoy contento', u'Me encuentro contento', u'Me siento contento']
        options = [u'¡Estupendo!', u'Me alegro de que estés contento']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)

    def test_estoy_positivo_different_feelings(self):
        questions = [u'Estoy feliz']
        options = [u'¡Estupendo!', u'Me alegro de que estés feliz']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)
        questions = [u'Me encuentro alegre']
        options = [u'¡Estupendo!', u'Me alegro de que estés alegre']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)     
        questions = [u'Me siento contento']
        options = [u'¡Estupendo!', u'Me alegro de que estés contento']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)     

    def test_estoybien(self):
        questions = [u'estoy bien', u'me encuentro bien', u'me siento bien']
        options = [u'Me alegro', u'Estupendo']
        for question in questions:
            assert tcs(question) in options
            assert assert_list( repeat_until(question, options), options)

    def test_estoy_otherthing(self):
        questions = [u'estoy cantando', u'pues estoy hablando contigo']
        options = [u'¿Por qué estás cantando?', u'¿Por qué estás hablando contigo?']
        for question in questions:
            assert tcs(question) in options

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
        options = [u"Yo soy Duke. ¿Tú como te llamas?", u"Me llamo Duke y soy un bot asistente para ayudarte con tus preguntas.", u"Duke, encantado de conocerte. Soy un bot especializado en java", u"Duke es mi nombre. Responder tus dudas yo debo"]
        assert tcs(question) in options
        assert assert_list( repeat_until(question, options), options)

    def test_sabes_hacer(self):
        questions = [u'que sabes hacer', u'que pues hacer', u'muestrame que sabes hacer', u'dime que puedes hacer']
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
        options = [u"Un bot asistente es como un diccionario parlante, te contesta preguntas si las sabe", u"Un bot asistente es un programa que simula a un humano teniendo una conversación. Además te contesta a preguntas si las sabe"]
        assert tcs(u'que es un bot asistente') in options
        assert tcs(u'preguntas sobre que') == u"En mi caso sobre Java"
        assert tcs(u'solo eso') == u'Me gustaria aprender más'        
        # iter 2
        options = [u"Un bot es como un diccionario parlante, te contesta preguntas si las sabe", u"Un bot es un programa que simula a un humano teniendo una conversación. Además te contesta a preguntas si las sabe"]
        assert tcs(u'que es un bot') in options
        assert tcs(u'que preguntas') == u"En mi caso sobre Java"
        # iter 2
        assert tcs(u'que es un bot') in options
        assert tcs(u'cualquier tipo de preguntas') == u"En mi caso sobre Java"

    def test_bot(self):
        options = [u"¿Preguntas lo que es? Un bot asistente es como un diccionario parlante, te contesta preguntas si las sabe", u"¿Preguntas lo que es? Un bot asistente es un programa que simula a un humano teniendo una conversación. Además te contesta a preguntas si las sabe"]
        assert tcs(u'bot asistente') in options
        assert tcs(u'preguntas sobre que') == u"En mi caso sobre Java"
        assert tcs(u'solo eso') == u'Me gustaria aprender más'        
        # iter 2
        options = [u"¿Preguntas lo que es? Un chatbot es como un diccionario parlante, te contesta preguntas si las sabe", u"¿Preguntas lo que es? Un chatbot es un programa que simula a un humano teniendo una conversación. Además te contesta a preguntas si las sabe"]
        assert tcs(u'chatbot') in options
        assert tcs(u'que preguntas') == u"En mi caso sobre Java"

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