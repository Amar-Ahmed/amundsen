import {DataAsset} from './DataAsset'

export interface DomainDetails {
    domain_contact: string;
    domain_data_asset: DataAsset[];
    domain_description: string;
    domain_name: string;
    domain_updates: string
}