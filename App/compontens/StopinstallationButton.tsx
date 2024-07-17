// StopinstallationButton.tsx
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Modal, Portal, Provider as PaperProvider } from 'react-native-paper';
import { useNavigation, NavigationProp } from '@react-navigation/native';
import { useState } from 'react';
import Icon from 'react-native-vector-icons/MaterialIcons';
import axios from 'axios';
import { ViewStyle } from 'react-native';

type RootStackParamList = {
  Start: undefined;
  // andere Routen hier hinzufügen
};

interface ItemAnalyzedProps {
    setScreen: (setScreen : boolean) => void; 
} 

export default function StopinstallationButton({setScreen}: ItemAnalyzedProps) { 
    const [visible, setVisible] = useState(false);
    const navigation = useNavigation<NavigationProp<RootStackParamList>>();

    const goToStartPage = () => {
        setScreen(true)
        navigation.navigate('Start');
        console.log('Navigating to Start page...');
        axios.delete(`http://${process.env.IP_ADRESS}:4000/stopProcess`)
            .then((response : any)  => {
                hideModal();
                console.log('Modal hidden after server response.');
                // Weitere Aktionen basierend auf der Antwort durchführen
            })
            .catch(error => {
                console.error('There was an error stopping the process:', error); // Fehlerbehandlung
                // Weitere Fehlerbehandlungen durchführen
            });
    };

    const showModal = () => {
        console.log('Show modal triggered');
        setVisible(true);
    };

    const hideModal = () => {
        console.log('Hide modal triggered');
        setVisible(false);
    };

    const containerStyle: ViewStyle = {
        backgroundColor: 'black',
        padding: 20,
        height: '60%',
        width: '90%',
        borderRadius: 20,
        alignSelf: 'center',
    };

    return (
        <View style={{ zIndex: 100, position: 'absolute', width: '100%', height: '80%' }}>
            <PaperProvider>
                <Portal>
                    <Modal visible={visible} onDismiss={hideModal} contentContainerStyle={containerStyle}>
                        <Text style={styles.modalText}>
                            Before cancelling the currently played story, please make sure, the installation is really empty!
                        </Text>
                        <View style={styles.buttonContainer}>
                            <Text style={styles.modalSubText}>
                                Are you sure you want to stop the installation?
                            </Text>
                            <TouchableOpacity onPress={goToStartPage} style={styles.iconButton}>
                                <Icon name="home" size={40} color="black" />
                            </TouchableOpacity>
                            <TouchableOpacity onPress={hideModal}>
                                <Text style={styles.closeModalText}>
                                    No, keep running
                                </Text>
                            </TouchableOpacity>
                        </View>
                    </Modal>
                </Portal>
                <View style={styles.iconContainerAbsolute}>
                    <TouchableOpacity onPress={showModal} style={styles.iconButton}>
                        <Icon name="home" size={40} color="black" />
                    </TouchableOpacity>
                </View>
            </PaperProvider>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        backgroundColor: '#000',
        justifyContent: 'center',
    },
    text: {
        position: 'absolute',
        top: '18%', 
        color: '#fff',
        fontFamily: '',
        fontSize: 18,
        letterSpacing: 14.4,
        lineHeight: 57.6,
        textAlign: 'center',
        textTransform: 'uppercase',
        width: '80%'
    },
    subtext: {
        position: 'absolute',
        bottom: '22%', 
        color: '#fff',
        fontFamily: '',
        fontSize: 14,
        letterSpacing: 14.4,
        lineHeight: 42,
        textAlign: 'center',
        textTransform: 'uppercase',
    },
    iconContainerAbsolute: {
        position: 'absolute', 
        bottom: '75%', 
        right: '35%',
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
    },
    iconButton: {
        width: 64,
        height: 64,
        backgroundColor: '#FFFFFF',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 32,
        marginVertical: 10,
    },
    buttonContainer: {
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
    },
    modalText: {
        color: 'white',
        fontFamily: '',
        fontSize: 24,
        textAlign: 'center',
    },
    modalSubText: {
        color: 'white',
        fontFamily: '',
        fontSize: 24,
        textAlign: 'center',
        marginVertical: 20,
    },
    closeModalText: {
        color: 'white',
        fontFamily: '',
        fontSize: 18,
        textAlign: 'center',
        textDecorationLine: 'underline',
        marginTop: 20,
    },
});
