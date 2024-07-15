import React from 'react';
import { View, Text, StyleSheet, ImageBackground, TouchableOpacity } from 'react-native';
import { Button, Modal, Portal, PaperProvider } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NavigationProp } from '@react-navigation/native'; 
import axios from 'axios';

interface ItemAnalyzedProps {
    navigation: NavigationProp<any>;
  }



export default function CurrentlyUsed({ navigation }: ItemAnalyzedProps) {
    const [visible, setVisible] = React.useState(false);

    

    const goToStartPage = () => {
        try {
            axios.delete(`http://${process.env.IP_ADRESS}:4000/stopProcess`)
                .then(response => {
                    // Erfolgreiche Antwort vom Server
                    console.log('Server response:', response.data);
                    hideModal();
                    // Hier können Sie weitere Aktionen basierend auf der Antwort durchführen
                })
                .catch(error => {
                    // Fehlerbehandlung
                    console.error('There was an error stopping the process:', error);
                    // Hier können Sie weitere Fehlerbehandlungen durchführen
                });
        } catch (error) {
            // Fehlerbehandlung
            console.error('There was an error stopping the process:', error);
        } finally { 
            navigation.navigate('Start');
        } 

    };
    

    const showModal = () => setVisible(true);
    const hideModal = () => setVisible(false);

    return (
        <ImageBackground 
            source={require('../images/decor6.png')} 
            style={styles.container}
        >
            <Text style={styles.text}>
                The installation 
                {'\n'}
                is currently 
                {'\n'}
                in use
                {'\n'}
            </Text>

            <Text style={styles.subtext}>
                is the 
                {'\n'}
                installation 
                {'\n'}
                unattanded?
            </Text>

            <View style={{width: '100%', height: "80%"}}>
                <PaperProvider>
                    <Portal>
                        <Modal visible={visible} onDismiss={hideModal} contentContainerStyle={styles.modal}>
                            <Text style={styles.modalText}>
                                Before cancelling the currently played story, please make sure, the installation is really empty!
                            </Text>
                            <View style={styles.buttonContainer}>
                                <Text style={styles.modalSubText}>
                                    Are you sure you want to stop the installation?
                                </Text>
                                <Button mode="contained" onPress={goToStartPage} style={styles.button} labelStyle={{ color: 'black', fontFamily: 'Helvetica', fontSize: 20, textTransform: 'uppercase',}}>
                                    Yes, Stop
                                </Button>
                                <TouchableOpacity onPress={hideModal}>
                                    <Text style={styles.closeModalText}>
                                        No, keep running
                                    </Text>
                                </TouchableOpacity>
                            </View>
                        </Modal>
                    </Portal>
                    <View style={styles.buttonContainerAbsolute}>
                        <Button
                            mode="contained"
                            onPress={showModal}
                            style={styles.button}
                            labelStyle={{ color: 'black', fontFamily: 'Helvetica', fontSize: 20, textTransform: 'uppercase',}}
                            >
                            Stop the installation
                        </Button>
                    </View>

                </PaperProvider>
            </View>
        </ImageBackground>
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
        fontFamily: 'Helvetica',
        fontSize: 18,
        letterSpacing: 14.4,
        lineHeight: 57.6,
        textAlign: 'center',
        textTransform: 'uppercase',
        width: '80%'
    },
    modal: {
        backgroundColor: 'black',
        padding: 20,
        height: '60%',
        width: '90%',
        borderRadius: 20,
        alignSelf: 'center',
    },
    subtext: {
        position: 'absolute',
        bottom: '22%', 
        color: '#fff',
        fontFamily: 'Helvetica',
        fontSize: 14,
        letterSpacing: 14.4,
        lineHeight: 42,
        textAlign: 'center',
        textTransform: 'uppercase',
    },
    buttonContainerAbsolute: {
        position: 'absolute', 
        bottom: "8%", 
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
    },
    button: {
        width: '80%',
        height: 64,
        backgroundColor: '#D7D3DB',
        justifyContent: 'center',
        marginVertical: 10,
    },
    buttonContainer: {
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
    },
    modalText: {
        color: 'white',
        fontFamily: 'Helvetica',
        fontSize: 24,
        textAlign: 'center',
    },
    modalSubText: {
        color: 'white',
        fontFamily: 'Helvetica',
        fontSize: 24,
        textAlign: 'center',
        marginVertical: 20,
    },
    closeModalText: {
        color: 'white',
        fontFamily: 'Helvetica',
        fontSize: 18,
        textAlign: 'center',
        textDecorationLine: 'underline',
        marginTop: 20,
    },
});
        