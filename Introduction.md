![](common/images/beagleboard-logo.svg)
# Please upgrade your software

Visit [bbb.io/upgrade](https://beagleboard.org/upgrade) to learn how

## Need to connect to a WiFi access point first?</p>
Use the command-line terminal block below to run the commands in bold, modifying as appropriate for your network.

```
debian@beaglebone:/var/lib/cloud9$ `**`sudo connmanctl&#x23CE;`**`
[sudo] password for debian: `**`temppwd&#x23CE;`**`
connmanctl> `**`scan wifi&#x23CE;`**`
Scan completed for wifi
connmanctl> `**`services&#x23CE;`**`
       MyWifi                  wifi_1234567890_1234567890123456_managed_psk
connmanctl> `**`agent on&#x23CE;`**`
Agent registered
connmanctl> `**`connect wifi_1234567890_1234567890123456_managed_psk&#x23CE;`**`
Agent RequestInput wifi_1234567890_1234567890123456_managed_psk
       Passphrase = [ Type=psk, Requirement=mandatory, Alternates=[ WPS ] ]
       WPS = [ Type=wpspin, Requirement=alternate ]
Passphrase? `**`MySecretPassphrase&#x23CE;`**`
Connected wifi_1234567890_1234567890123456_managed_psk
connmanctl> `**`quit&#x23CE;`**`
debian@beaglebone:/var/lib/cloud9$
```

Now you can click [bbb.io/upgrade](https://beagleboard.org/upgrade)
