
template_notify_subject = '[ModI-Governance]: Alert comunicazioni'

template_notify_ok = '''
<div style="padding: 2px 0px;">
    <p>Rilevante n. {n} nuove comunicazioni provenienti da indirizzi di RTD validi, di seguito la lista con gli oggetti delle comunicazioni:            
    <ul>{msg_list}</ul> 
</div>
'''
template_notify_ko = '''
<div style="padding: 2px 0px;">        
            <p>Rilevate n. {n} nuove comunicazioni scartate provenienti da indirizzi di RTD non validi, di seguito la lista con gli oggetti delle comunicazioni:
            <ul>{msg_list}</ul> 
</div>
'''

template_notify_end = '</div><p>Grazie</p></div>'


template_response_subject = '[ModI-Governance] Reply-to: {pec_sub} del {pec_when}'

template_response_ko = '''
<div style="padding: 2px 0px;">
    <p>La comunicazione a mezzo PEC del <strong>{pec_when}</strong> avente oggetto:</p> 
    <p><strong>{pec_sub}</strong></p> 
    <p>non &egrave; stata presa in carico.</p>
    <p>L'indirizzo mittente <strong>{pec_from}</strong> non risulta essere un indirizzo di un RTD(Responsabile per la Transizione al Digitale) registrato in IPA (Indice dei domicili digitali delle Pubbliche Amministrazioni e dei Gestori di Pubblici Servizi)</p>
    <p>Si prega di utilizzare un indirizzo di un RTD valido.</p>
    <p>Grazie</p>
</div>
'''