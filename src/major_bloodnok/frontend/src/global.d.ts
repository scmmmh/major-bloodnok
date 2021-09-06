/// <reference types="svelte" />

interface JSONAPIItem {
    type: string;
    id: string;
    attributes?: JSONAPIItemAttributes;
}

interface JSONAPIItemAttributes {
    [x: string]: string | number;
}

interface Transaction {
    type: string;
    id: string;
    attributes: TransactionAttributes;
}

interface TransactionAttributes {
    title: string;
    description: string;
    date: Date;
    amount: number;
    direction: string;
    initiator: string
}
