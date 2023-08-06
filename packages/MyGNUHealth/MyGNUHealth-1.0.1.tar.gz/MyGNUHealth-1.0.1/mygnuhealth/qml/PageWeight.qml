// SPDX-FileCopyrightText: 2020-2021 GNU Solidario <health@gnusolidario.org>
//                         2020-2021 Luis Falcon <falcon@gnuhealth.org>
//                         2021-2021 Carl Schwan <carlschwan@kde.org>
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick 2.7
import org.kde.kirigami 2.10 as Kirigami
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
import Weight 0.1

Kirigami.Page {
    id: weightpage
    title: qsTr("Body Weight")

    Weight { // Weight object registered at mygh.py
        id: body_weight
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
            id: weightIcon
            height: parent.height
            anchors.centerIn: parent
            source: "../images/weight-icon.svg"
            fillMode: Image.PreserveAspectFit
        }
    }

    ColumnLayout{
        anchors.centerIn: parent


        Label {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Body Weight (kg)")
            font.bold: true
        }
        Slider {
            id: sliderweight
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            from: 1
            to: 200
            stepSize: 0.1
            wheelEnabled: true
            value: body_weight.last_weight

        }

        TextField {
            id: textweight
            Layout.alignment: Qt.AlignHCenter
            text: sliderweight.value.toFixed(1)
            horizontalAlignment: TextInput.Center
            maximumLength: 5
            inputMethodHints: Qt.ImhDigitsOnly
            onEditingFinished: sliderweight.value = Number(textweight.text)
            color: acceptableInput ? "black" : "red"
        }

        Label {
            id: weightpounds
            property int wpounds: sliderweight.value * (2.204623)
            Layout.alignment: Qt.AlignHCenter
            text: wpounds + " lb"
        }

        Button {
            text: qsTr("Set")
            Layout.alignment: Qt.AlignHCenter
            icon.name: "list-add"
            onClicked: body_weight.getvals(sliderweight.value.toFixed(1))
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
