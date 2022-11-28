
template_notify_subject='[ModI-Governance]: Alert comunicazioni'

template_notify = '''
<html>
    <body>
        <div>{}</div>
        <div>{}</div>
    </body>
</html>       
'''

template_notify_ok='''
<div style="padding: 2px 0px;display={}">
    <p>Ci sono n. {} nuove comunicazioni provenienti da indirizzi di RTD validi, di seguito la lista con gli oggetti delle comunicazioni:            
    <ul>{}</ul> 
    <p>Grazie</p>
</div>
'''

template_notify_ko = '''
<div style="padding: 2px 0px;display={}">
            <p>Ci sono n. {} nuove comunicazioni scartate provenienti da indirizzi di RTD non validi, di seguito la lista con gli oggetti delle comunicazioni:
            <ul>{}</ul> 
            <p>Grazie</p>
</div>
'''

template_response_subject = '[ModI-Governance] Reply-to: {} del {}'

template_response_ok = '''
<html>
    <body>
        <div style="padding: 2px 0px;">
            <p>La comunicazione a mezzo PEC del <strong>{}</strong> avente oggetto: <strong>{}</strong> non &egrave; è stata presa in carico.</p>
            <p>Per eventuali comunicazioni ulteriori in merito, sara utilizzato l'indirizzo mittente dalla comunicazione.            
            <p>Grazie</p>
        </div>
    </body>
</html>
'''

template_response_ko = '''
<html>
    <body>
        <div style="padding: 2px 0px;">
            <p>La comunicazione a mezzo PEC del <strong>{}</strong> avente oggetto: <strong>{}</strong> non &egrave; stata presa in carico.</p>
            <p>L'indirizzo mittente <strong>{}</strong> non risulta essere un indirizzo di un RTD(Responsabile per la Transizione al Digitale) registrato in IPA (Indice dei domicili digitali delle Pubbliche Amministrazioni e dei Gestori di Pubblici Servizi)</p>
            <p>Si prega di utilizzare un indirizzo di un RTD valido.</p>
            <p>Grazie</p>
        </div>
    </body>
</html>
'''