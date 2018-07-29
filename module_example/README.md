# Notizen
Eine lose Sammlung an Notizen zum schreiben von eigenen ansible Modulen:
  * Das Schlüsselwort im Playbook wird über den Dateinamen vom Modul festgelegt
  * Ein ``exit_json`` oder ``fail_json`` beendet das Modul
  * Der Pfad zum Modul wird entweder in der ``/etc/ansible/ansible.cfg``, ``~/.ansible.cfg``, ``/path/to/project/ansible.cfg`` oder per Parameter ``--path=/path/to/module`` übergeben
