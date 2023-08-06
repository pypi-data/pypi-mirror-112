import QtQuick 2.7
import org.kde.kirigami 2.5 as Kirigami
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import Osat 0.1

Kirigami.Page
{
id: glucosePage
title: qsTr("Oxygen Saturation")

    Osat { // Osat object registered at main.py
        id: hb_osat
        onSetOK: {
            /* We pop the current page from the stack and immediately
            /  replace the Biopage to refresh its contents
            */
            pageStack.pop()
            pageStack.replace(Qt.resolvedUrl("PageBio.qml"))
        }
    }

    Rectangle {
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        color: "#136f84"
        height: 80
        width: parent.width
        radius: 10
        Image {
            id: osatIcon
            height: parent.height
            anchors.centerIn: parent
            source: "../images/osat-icon.svg"
            fillMode: Image.PreserveAspectFit
        }
    }

    ColumnLayout {
        id: content
        spacing: 10
        anchors.centerIn: parent

        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Oxygen Saturation")
            font.bold: true
        }

        SpinBox {
            id: osat
            Layout.preferredHeight: 100
            Layout.preferredWidth: 150
            font.pixelSize:30
            from: 50
            to: 99
            value:99
            editable: false
            wheelEnabled: true
        }


        Button {
            id: buttonSetOsat
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Set")
            flat: false
            onClicked: {
                hb_osat.getvals(osat.value);
            }

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
