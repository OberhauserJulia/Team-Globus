import React, { useEffect } from "react";
import { View, Text, ImageBackground, StyleSheet } from 'react-native';
import { ActivityIndicator } from 'react-native-paper';
import axios from "axios";
import { useItem } from "../context/ItemContext";
import StopinstallationButton from "../compontens/StopinstallationButton";
import { NavigationProp } from '@react-navigation/native';



interface ItemAnalyzedProps {
    navigation: NavigationProp<any>;
  }

export default function AnalyzingProgress({ navigation }: { navigation: NavigationProp<any> }) {
    const { item, setItem } = useItem();

    useEffect(() => {
        axios.post<{ data: any }>('http://192.168.119.190:4000/api/placeitem')
            .then((response: any) => {
                console.log('Success:', response.data);
                setItem(response.data.data);
                navigation.navigate('ItemAnalyzed');
            })
            .catch((error: Error) => {
                console.error('Error:', error);
                navigation.navigate('AnalyzingProgress');
            });
    }, [navigation]);

    return (
        
        <ImageBackground 
            source={require('../images/decor3.png')} 
            style={styles.container}
        >
            <Text style={styles.text}>
                Item is
                {'\n'}
                being 
                {'\n'}
                analyzed
            </Text>

            <ActivityIndicator animating={true} color={'#D7D3DB'} size={80} />

            <Text style={styles.subtext}>
                please wait
                {'\n'}
                a moment
            </Text>
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
        top: '15%', 
        color: '#fff',
        fontFamily: 'Helvetica',
        fontSize: 18,
        letterSpacing: 14.4,
        lineHeight: 57.6,
        textAlign: 'center',
        textTransform: 'uppercase',
    },
    subtext: {
        position: 'absolute',
        bottom: '15%', 
        color: '#fff',
        fontFamily: 'Helvetica',
        fontSize: 14,
        letterSpacing: 14.4,
        lineHeight: 42,
        textAlign: 'center',
        textTransform: 'uppercase',
    },
});
