var Boot=99
var AnlagenKWP=78360
var time_start = new Array(8,8,6,6,6,5,5,6,7,7,7,8)
var time_end = new Array(17,18,20,21,21,22,22,21,20,19,17,17)
var sollMonth = new Array(2,6,9,11,11,13,13,12,10,6,4,3)
var SollYearKWP=950
var AnzahlWR = 11
var MaxWRP=new Array(AnzahlWR)
MaxWRP[0]=new Array(8600,75000,1300000,10000000)
MaxWRP[1]=new Array(8600,75000,1300000,10000000)
MaxWRP[2]=new Array(8600,75000,1300000,10000000)
MaxWRP[3]=new Array(8600,75000,1300000,10000000)
MaxWRP[4]=new Array(8600,75000,1300000,10000000)
MaxWRP[5]=new Array(8600,75000,1300000,10000000)
MaxWRP[6]=new Array(8600,75000,1300000,10000000)
MaxWRP[7]=new Array(8600,75000,1300000,10000000)
MaxWRP[8]=new Array(5900,50000,900000,7000000)
MaxWRP[9]=new Array(5900,50000,900000,7000000)
MaxWRP[10]=new Array(5900,50000,900000,7000000)
var WRInfo = new Array(AnzahlWR)
WRInfo[0]=new Array("PAC7","  10002579",7800,1,"WR 1",1,null,null,0,null,14,0,1,1000,null)
WRInfo[0][16]=1
WRInfo[0][17]=1
WRInfo[1]=new Array("PAC7","  10002581",7800,1,"WR 2",1,null,null,0,null,14,0,1,1000,null)
WRInfo[1][16]=1
WRInfo[1][17]=1
WRInfo[2]=new Array("PAC7","  29100136",7800,1,"WR 3",1,null,null,0,null,14,0,1,1000,null)
WRInfo[2][16]=1
WRInfo[2][17]=1
WRInfo[3]=new Array("PAC7","  27103494",7800,1,"WR 4",1,null,null,0,null,14,0,1,1000,null)
WRInfo[3][16]=1
WRInfo[3][17]=1
WRInfo[4]=new Array("PAC7","  50000254",7800,1,"WR 5",1,null,null,0,null,14,0,1,1000,null)
WRInfo[4][16]=1
WRInfo[4][17]=1
WRInfo[5]=new Array("PAC7","  27103399",7800,1,"WR 6",1,null,null,0,null,14,0,1,1000,null)
WRInfo[5][16]=1
WRInfo[5][17]=1
WRInfo[6]=new Array("PAC7","  10002578",7800,1,"WR 7",1,null,null,0,null,14,0,1,1000,null)
WRInfo[6][16]=1
WRInfo[6][17]=1
WRInfo[7]=new Array("PAC7","  27103475",7800,1,"WR 8",1,null,null,0,null,14,0,1,1000,null)
WRInfo[7][16]=1
WRInfo[7][17]=1
WRInfo[8]=new Array("4800 TL","1002.100721007",5320,1,"WR 9",1,null,null,0,null,19,0,0,1000,null)
WRInfo[8][16]=2
WRInfo[8][17]=1
WRInfo[9]=new Array("4800 TL","1001.100721121",5320,1,"WR 10",1,null,null,0,null,19,0,0,1000,null)
WRInfo[9][16]=2
WRInfo[9][17]=1
WRInfo[10]=new Array("4800 TL","1002.100721002",5320,1,"WR 11",1,null,null,0,null,19,0,0,1000,null)
WRInfo[10][16]=2
WRInfo[10][17]=1
var HPTitel=""
var HPBetreiber=""
var HPEmail=""
var HPStandort=""
var HPModul=""
var HPWR="Diel Ako 4800TL / Oelmaier Pac7"
var HPLeistung=""
var HPInbetrieb=""
var HPAusricht=""
var BannerZeile1=""
var BannerZeile2=""
var BannerZeile3=""
var BannerLink=""
var StatusCodes = new Array(11)
var FehlerCodes = new Array(11)
StatusCodes[0] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[0] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[1] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[1] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[2] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[2] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[3] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[3] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[4] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[4] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[5] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[5] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[6] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[6] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[7] = "Warten,Standby Betrieb,Inbetriebsetzung,MPP,Leistungsbegrenzung,Warten, , , "
FehlerCodes[7] = " ,Fehler AFI,Isolationsfehler,Fehler DC-Offset, , , , , ,Fehler Uac L1 Master,Fehler Uac L2 Master,Fehler Uac L3 Master,Fehler Udc Master,Fehler Freq. Master,Fehler Netzrelais Master, , ,Fehler Uac L1 Slave,Fehler Uac L2 Slave,Fehler Uac L3 Slave,Fehler Udc Slave,Fehler Freq. Slave,Fehler Netzrelais Slave, ,Fehler"
StatusCodes[8] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[8] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[9] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[9] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
StatusCodes[10] = "Standby,Warte DC-Spannung,Warte Netz,MPP,Vorlast,Fehler,Undefined"
FehlerCodes[10] = " ,allg. Systemfehler,Konsistenz AC-Spannung,Konsistenz Frequenz,E-103,E-104,E-105,E-106,E-107,E-108,Relais,E-111,E-112,Versionskonflikt,GMU nicht kalibriert,Keine Ident.daten ICU,Keine Ident.daten GMU,Ident.daten UI-ICU nicht gleich,Ident.daten GMU-ICU nicht gleic,E-126,E-127,E-128,E-129,E-130,E-131,E-132,E-133,E-134,E-140,E-141,E-150,E-180,allg. Fehler,Amplitude L1,Amplitude L12,Amplitude L23,Amplitude L13,durchgang L1-2,durchgang L1-3,Interrupt L2 oder L3 fehlt,Amplitude L1 Schnellabschalt.,E-209,Frequenz L1 (GMU),Frequenz L1 (ICU),Synchronisierung ICU,E-213,E-214,E-215,E-216,E-217,E-218,E-219,T_IGBT,T_Coil,T_PCB,E-223,E-224,E-225,E-226,Sensor IGBT,Sensor Drossel,Sensor PCB,E-233,E-234,E-235,E-236,E-237,E-238,E-239,DC Überspannung,DC Überstrom,E-242,E-245,E-246,Kommunikation GMU-ICU,Kommunikation UI-ICU,SD,Versorgung ICU,Relaistest,E-255,E-256,E-257,E-258,E-259,UI Reset,E-261,E-270,E-280,E-290,E-299,lange keine Einspeisung,abrupter DC-Spannungsabfall,E-351,E-400,E-401,E-402,E-403,E-410,E-411,E-412,E-413,E-414,E-421,E-422,E-430,E-450,undefined,Unbekannt (Neuer Fehler),Installationsfehler,allgemeiner Systemfehler,interne Systemmeldung,Information,UAC zu hoch E-90,UDC zu hoch E-91,DC verpolt E-92,Isolationsfehler PV_GND E-93,Systemfehler E-94,Systemfehler E-95,UnDeFiNeD"
var Verguetung=3914
var Serialnr = 277952088
var Firmware = "4.2.7 Build 116"
var FirmwareDate = "19.02.2020"
var WRTyp = "MULTIPROTOCOL"
var OEMTyp = 0
var SLTyp = "1200"
var SLVer = 2
var SLHW = 10147164
var SLBV = 40
var Intervall = 300
var SLDatum = "22.07.23"
var SLUhrzeit = "04:15:13"
var isTemp=true
var isOnline=true
var eventsHP=1
var exportDir=""
var Lang="DE"
var AnzahlGrp=0
var CFDatum = "19.07.23"
var CFUhrzeit = "13:52:59"
var SCB = true
var SCBIF1 = 0
var webMenuFull = 0
var IPlatform = 3
var DateFormat ="dd.mm.yy"
var TimeFormat ="HH:MM:ss"
var TimeFormatNoSec ="HH:MM"
var Currency ="€"
var CurrencySub ="Cent"
var CurrencyFirst ="0"
var ISOCode ="DE"
var DSTMode ="1"
var Dezimalseparator =","
var WeightUnit ="KG"
var DirectMarketing = false
var AdamAvailable=0
var netProfile=0
var pmControlType=1
var pmReductionOnSerialType=3
var windinverters=0
var co2factor=700
