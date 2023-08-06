import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import org.kde.kirigami 2.5 as Kirigami
import PoL 0.1

Kirigami.Page {
    id: pageoflife
    title: qsTr("New Page of Life")

    header: Control {
        padding: Kirigami.Units.smallSpacing
        contentItem: Kirigami.InlineMessage {
            id: errorMessage
            visible: false
            text: pol.msg
            type: Kirigami.MessageType.Error
            showCloseButton: true
        }
    }

    PoL { // Object registered at mygh.py to be used here
        id: pol
        property var errors: {
            "wrongdate": qsTr("Wrong date"),
            "successcreate": qsTr("OK!"),
            "rsnotfound": qsTr("RefSNP not found"),
        }
        property var msg: ""
        
        onWrongDate: {
            msg = errors["wrongdate"]
            errorMessage.visible = true;
        }

        onCreateSuccess: {
           pageStack.pop() // Return to Book of Life
           pageStack.replace(Qt.resolvedUrl("PageBol.qml")) // Refresh
        }

        onRsNotfound: {
            msg = errors["rsnotfound"]
            errorMessage.visible = true;
        }
    }

    Rectangle {
        id: rectheader
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        color: "#136f84"
        height: 60
        width: parent.width
        radius: 5
        Image {
            id: glucoseIcon
            height: parent.height
            anchors.centerIn: parent
            source: "../images/activity-square-icon.svg"
            fillMode: Image.PreserveAspectFit
        }
    }


    ColumnLayout {
        id:polarea
        anchors.horizontalCenter: rectheader.horizontalCenter
        anchors.top: rectheader.bottom
        anchors.topMargin: 5

        RowLayout {
            id:dateitem
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            spacing: 2
            property var datenow: pol.todayDate

            Label {
                id:pagedate
                text: qsTr("Date")
            }
            TextField {
                id: calday
                placeholderText: qsTr("dd")
                horizontalAlignment: TextInput.Center
                Layout.preferredWidth: 40
                maximumLength: 2
                text: dateitem.datenow[0]
                inputMethodHints: Qt.ImhDigitsOnly
                validator: IntValidator {bottom: 1; top: 31;}
                color: acceptableInput ? "black" : "red"
            }

            TextField {
                id: calmonth
                placeholderText: qsTr("mm")
                horizontalAlignment: TextInput.Center
                text: dateitem.datenow[1]
                Layout.preferredWidth: 40
                maximumLength: 2
                inputMethodHints: Qt.ImhDigitsOnly
                validator: IntValidator {bottom: 1; top: 12}
                color: acceptableInput ? "black" : "red"
            }

            TextField {
                id: calyear
                placeholderText: qsTr("yyyy")
                horizontalAlignment: TextInput.Center
                Layout.preferredWidth: 50
                text: dateitem.datenow[2]
                inputMethodHints: Qt.ImhDigitsOnly
                maximumLength: 4
                validator: IntValidator {bottom: 1900; top: dateitem.datenow[2]}
                color: acceptableInput ? "black" : "red"
            }

            Label {
                Layout.leftMargin: 10
                id:pagetime
                text: qsTr("Time")
            }


            TextField {
                id: calhour
                text: dateitem.datenow[3]
                Layout.preferredWidth: 40
                horizontalAlignment: TextInput.Center
                validator: IntValidator {bottom: 1; top: 23}
                color: acceptableInput ? "black" : "red"
            }
            TextField {
                id: calminute
                text: dateitem.datenow[4]
                Layout.preferredWidth: 40
                horizontalAlignment: TextInput.Center
                validator: IntValidator {bottom: 0; top: 59}
                color: acceptableInput ? "black" : "red"
            }
        }


    // Title of the Page of Life (summary)
        RowLayout {
            id: titleform
            Layout.fillWidth: true
            TextField {
                id:summary
                Layout.fillWidth: true
                placeholderText: qsTr("Summary")
                focus: true
            }
        }


        // Health domain and context
        ColumnLayout {
            id: domainrow
            ComboBox {
                id: domainid
                model: pol.poldomain
                textRole: "text"
                valueRole: "value"
                onActivated: pol.update_context(domainid.currentValue)
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Domain")
            }
            ComboBox {
                id: contextid
                model: pol.polcontext
                textRole: "text"
                valueRole: "value"
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Context in the domain")
            }

            ComboBox {
                id: relevance
                textRole: "text"
                valueRole: "value"
                model: [
                    { value: "normal", text: qsTr("Normal") },
                    { value: "important", text: qsTr("Important") },
                    { value: "critical", text: qsTr("Critical") }
                ]
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Relevance")
            }
            CheckBox {
                id: privatePage
                checked: false
                text: qsTr("Private")
            }

        }
        
        // Item reserved for genetic information
        // It will be shown only when the medical domain context is Genetics 
        GridLayout {
            id: geneticsgrid
            visible: contextid.currentValue === 'genetics'
            Layout.preferredWidth: rectheader.width
            columns: 2
            TextField {
                id:rsid
                property var rs: pol.polrs
                placeholderText: qsTr("RefSNP")
                horizontalAlignment: TextInput.Center
                Layout.preferredWidth: rectheader.width/2
                onEditingFinished: {
                    pol.checkSNP(rsid.text)
                    geneid.text = pol.polrs.gene
                    aachange.text = pol.polrs.aa_change
                    variantid.text = pol.polrs.variant
                    proteinid.text = pol.polrs.protein
                    significance.text = pol.polrs.significance
                    disease.text = pol.polrs.disease
                }
            }
            TextField {
                id:proteinid
                Layout.preferredWidth: rectheader.width/2
                placeholderText: qsTr("Protein ID")
                horizontalAlignment: TextInput.Center
                readOnly: true
            }

            TextField {
                id:geneid
                placeholderText: qsTr("Gene")
                Layout.preferredWidth: rectheader.width/2
                horizontalAlignment: TextInput.Center
                readOnly: true
            }
            TextField {
                id:aachange
                Layout.preferredWidth: rectheader.width/2
                placeholderText: qsTr("AA change")
                horizontalAlignment: TextInput.Center
                readOnly: true
            }
            TextField {
                id:variantid
                Layout.preferredWidth: rectheader.width/2
                placeholderText: qsTr("Variant")
                horizontalAlignment: TextInput.Center
                readOnly: true
            }
            TextField {
                id:significance
                Layout.preferredWidth: rectheader.width/2
                placeholderText: qsTr("Significance")
                horizontalAlignment: TextInput.Center
                readOnly: true
            }
            TextField {
                id:disease
                Layout.columnSpan: 2
                Layout.fillWidth: true
                placeholderText: qsTr("Disease")
                horizontalAlignment: TextInput.Center
                readOnly: true
            }
        }
        TextArea {
            id:information
            Layout.fillWidth: true
            Layout.preferredHeight: 70
            placeholderText: qsTr("Enter details here")
            wrapMode: TextEdit.WordWrap
        }
        
        Button {
            id: buttonKey
            /* Type casting to int the values from the date
                * that are strings and may include valid entries such
                * as prefixing zeros (like "03") in months and days
                */
            property int pyear: calyear.text
            property int pmonth: calmonth.text
            property int pday: calday.text
            property int phour: calhour.text
            property int pminute: calminute.text

            property var page_date: [pyear, pmonth, pday, phour, pminute]
            property var genetic_info: [rsid.text, geneid.text, aachange.text,  variantid.text, proteinid.text, significance.text, disease.text]
            onClicked: pol.createPage(page_date, domainid.currentValue, contextid.currentValue,relevance.currentValue, privatePage.checked,
                                      genetic_info, summary.text, information.text)
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Create")
        }
    }

   footer: Rectangle{
            id: rectfooter
            width: parent.width
            height: 40
            Image {
                id: myghIcon
                anchors.centerIn: rectfooter
                source: "../images/myGH-horizontal-icon.svg"
                width: 160
                fillMode: Image.PreserveAspectFit
            }
        }


}
