from ansible.module_utils.basic import AnsibleModule
import os
import tempfile
import urllib2
import tarfile

ANSIBLE_METADATA = {
    'metadata_version': 0.1,
    'status': ['preview'],
    'supported_by': 'Dan Steffen'
}

DOCUMENTATION = '''
module: url_extract_module

short_description: Demo-Module fuer den download und das auspacken einer Datei

description:
    - "Modul zum herunterladen und auspacken von Dateien von einer URL"

author:
    - Dan Steffen (dan.steffen.de@gmail.com)
'''

EXAMPLES = '''
# Get file test.tar from example.com and extract it to the directory /path/to/dir
- name: Get file from example.com
  url_extract:
    url: http://example.com/test.tar
    dest: /path/to/dir
'''

RETURN = '''
    tbd
'''

def main():
    # Definition der Parameter fuer das Module
    module_args = dict(
        url=dict(type='str', required=True),
        dest=dict(type='str', required=True)
    )

    # Erstellen des Objektes fuer die Interaktion mit ansible
    module = AnsibleModule (
      argument_spec=module_args,
	  supports_check_mode=True
    )

    # Assoziatives Array mit den Rueckgabewerten aus dem Modul
    result=dict(
        changed=False,
        message=''
    )

    # Tests fuer einen dry-run
    if module.check_mode:
        # Pruefe ob das ein Verzeichnis oder Datei mit dem Zielnamen existiert
        if os.path.exists(module.params['dest']):
            # Pruefe ob es sich um ein Verzeichnis handelt und ob dieses schreibbar ist
            if not os.path.isdir(module.params['dest']):
                module.fail_json(msg="Destination is not a directory")
            else:
                if not os.access(module.params['dest'], os.W_OK):
                    module.fail_json(msg="Destination is not writable")

        # Pruefe ob Quelldatei existiert
        try:
            url_handler = urllib2.urlopen(module.params['url'])
        except urllib2.HTTPError as e:
            module.fail_json(msg="A HTTP error has occurred")
        module.exit_json(**result)

    # Behandlung der Modul-Parameter
    #
    # dest: Pruefe ob das Ziel-Verzeichnis u.U. existiert, sonst
    #       lege es an
    if os.path.exists(module.params['dest']):
        if not os.path.isdir(module.params['dest']):
            module.fail_json(msg="Destination is not a directory")
    else:
        # Erstellen von dem Verzeichnis falls es nicht existiert
        try:
            os.makedirs(module.params['dest'])
        except OSError as e:
            module.fail_json(msg="Could not create directory "+module.params['dest'])

    # url: Herunterladen und entpacken der angegebenen Datei
    try:
        url_handler = urllib2.urlopen(module.params['url'])

        # Anlegen einer temporaeren Datei fuer den heruntergeladenen Inhalt
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(url_handler.read())

        # Entpacken der Datei in das Zielverzeichnis
        tar = tarfile.open(tmp_file.name)
        tar.extractall(path=module.params['dest'])
    except urllib2.HTTPError as e:
        module.fail_json(msg="A HTTP error has occurred")
    except tarfile.TarError as e:
         module.fail_json(msg="An unpack error has occurred")
    finally:
         # Schliessen der Filehandler und setzen der Erfolgs-Nachricht
         url_handler.close()
         tmp_file.close()
         tar.close()
         result['changed']=True
         result['message']='File successfully downloaded from '+module.params['url']+' and extract to '+module.params['dest']

    # Task war erfolgreich
    module.exit_json(**result)

if __name__ == '__main__':
    main()