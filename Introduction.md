![](common/images/beagleboard-logo.svg)
# Please upgrade your software

Visit [bbb.io/upgrade](https://beagleboard.org/upgrade) to learn how

## Need to connect to a WiFi access point first?</p>
Use the command-line terminal block below to run the commands in bold, modifying as appropriate for your network.

<pre>
debian@beaglebone:/var/lib/cloud9$ <b>sudo connmanctl&#x23CE;</b>
[sudo] password for debian: <b>temppwd&#x23CE;</b>
connmanctl> <b>scan wifi&#x23CE;</b>
Scan completed for wifi
connmanctl> <b>services&#x23CE;</b>
       MyWifi                  wifi_1234567890_1234567890123456_managed_psk
connmanctl> <b>agent on&#x23CE;</b>
Agent registered
connmanctl> <b>connect wifi_1234567890_1234567890123456_managed_psk&#x23CE;</b>
Agent RequestInput wifi_1234567890_1234567890123456_managed_psk
       Passphrase = [ Type=psk, Requirement=mandatory, Alternates=[ WPS ] ]
       WPS = [ Type=wpspin, Requirement=alternate ]
Passphrase? <b>MySecretPassphrase&#x23CE;</b>
Connected wifi_1234567890_1234567890123456_managed_psk
connmanctl> <b>quit&#x23CE;</b>
debian@beaglebone:/var/lib/cloud9$
</pre>

Now you can click [bbb.io/upgrade](https://beagleboard.org/upgrade)
