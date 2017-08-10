BLINKTEMP
--------------------
### Visual CPU Temperature indicator

Python Daemon for Raspberry Pi

----

### Installation

1.  Clone it
2.  Run install.sh as the superuser
3.  Reboot your Raspberry Pi
4.  Enjoy your fresh Blinktemp!
------

### Configuration

1.  Setting your own temperature range.

    To set your own temperature range, first stop the service.

    ```sudo systemctl stop blinktemp```

    Next, open ``blinktemp.sh``` in a text editor, like so:

       nano ./blinktemp.sh

    from your download directory.  Make a few changes to DAEMON_OPTS:

    ```
    -tb [integer]     - option to set the lower temperature range
    -tl [integer]     - option to set the upper temperature range  
    ```

    **Example:**

        ```DAEMON_OPTS="-tb 32 -tl 79"

    Now run ```sudo ./install.sh``` again to re-install, update, and restart the service.  