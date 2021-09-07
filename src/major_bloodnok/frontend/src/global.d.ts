/// <reference types="svelte" />

interface JSONAPIItem {
    type: string;
    id: string;
    attributes?: JSONAPIItemAttributes;
    relationships?: JSONAPIItemRelationships;
}

interface JSONAPIItemAttributes {
    [x: string]: string | number;
}

interface JSONAPIItemRelationships {
    [x: string]: JSONAPIItemRelationship;
}

interface JSONAPIItemRelationship {
    data: JSONAPIItemRelationshipData;
}

interface JSONAPIItemRelationshipData {
    type: string;
    id: string;
}

interface Transaction {
    type: 'transactions';
    id: string;
    attributes: TransactionAttributes;
    relationships: JSONAPIItemRelationships;
}

interface TransactionAttributes {
    title: string;
    description: string;
    date: Date;
    amount: number;
    direction: string;
    initiator: string
}

interface Category {
    type: 'categories';
    id: string;
    attributes: CategoryAttributes;
    relationships: CategoryRelationships;
}

interface CategoryAttributes {
    title: string;
}

interface CategoryRelationships {
    parent?: JSONAPIItemRelationship;
}
