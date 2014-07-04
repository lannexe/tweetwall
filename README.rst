Comment installer le tweetwall de la cantine ?

C'est parti::

   $ virtualenv venv
   $ source venv/bin/activate
   $ pip install -r requirements.txt
   
Si vous avez l'erreur suivante lors de l'installation des requirements sous (MAC OS) ::

   $ fatal error: 'X11/Xlib.h' file not found

Vous devez installer le command line developer tools de xcode

   $ xcode-select --install

