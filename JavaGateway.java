import py4j.GatewayServer;
import java.util.*;

import java.io.*;
import org.w3c.dom.Element;
import oasis.names.tc.saml._2_0.protocol.AttributeQuery;
import be.ehealth.technicalconnector.config.ConfigFactory;
import be.ehealth.technicalconnector.service.sts.domain.SAMLAttribute;
import be.ehealth.technicalconnector.service.sts.domain.SAMLAttributeDesignator;
import be.ehealth.technicalconnector.service.sts.security.SAMLToken;
import be.ehealth.technicalconnector.session.Session;
import be.ehealth.technicalconnector.session.SessionManager;
import be.ehealth.technicalconnector.config.ConfigValidator;
import be.ehealth.businessconnector.genericasync.mappers.CommonInputMapper;
import org.mapstruct.factory.Mappers;
import be.ehealth.business.mycarenetdomaincommons.domain.Attribute;
import be.ehealth.businessconnector.genericasync.session.GenAsyncSessionServiceFactory;
import be.ehealth.technicalconnector.utils.ConnectorIOUtils;
import java.nio.charset.StandardCharsets;
// import java.sql.Blob;
import be.ehealth.business.mycarenetdomaincommons.domain.Blob;

import static java.nio.charset.StandardCharsets.UTF_8;
import be.ehealth.technicalconnector.exception.ConnectorException;
import be.ehealth.business.mycarenetdomaincommons.domain.McnPackageInfo;
import be.ehealth.business.mycarenetdomaincommons.util.McnConfigUtil;
import be.ehealth.business.mycarenetdomaincommons.util.WsAddressingUtil;
import be.ehealth.business.mycarenetdomaincommons.builders.CommonBuilder;
import be.ehealth.business.mycarenetdomaincommons.builders.RequestBuilderFactory;
import be.ehealth.businessconnector.test.testcommons.utils.FileTestUtils;
import be.cin.nip.async.generic.*;
import java.net.URI;
import be.ehealth.technicalconnector.handler.domain.WsAddressingHeader;
import be.ehealth.businessconnector.genericasync.exception.GenAsyncBusinessConnectorException;
import be.ehealth.technicalconnector.exception.TechnicalConnectorException;
import be.ehealth.technicalconnector.exception.SessionManagementException;
import java.net.URISyntaxException;
import be.ehealth.businessconnector.genericasync.session.GenAsyncService;
import be.cin.mycarenet.esb.common.v2.OrigineType;
import org.slf4j.LoggerFactory;
import be.ehealth.technicalconnector.idgenerator.IdGeneratorFactory;
import org.slf4j.Logger;
import be.cin.nip.async.generic.Confirm;
import be.ehealth.businessconnector.mycarenet.agreement.builders.impl.EncryptedRequestObjectBuilderImpl;
import be.ehealth.businessconnector.mycarenet.agreement.exception.AgreementBusinessConnectorException;
import be.ehealth.business.mycarenetdomaincommons.domain.InputReference;
import be.ehealth.business.common.domain.Patient;
import org.joda.time.DateTime;
import be.ehealth.businessconnector.mycarenet.agreement.domain.AskAgreementBuilderRequest;
import be.ehealth.businessconnector.mycarenet.agreement.domain.AgreementBuilderRequest;
import be.ehealth.business.mycarenetdomaincommons.builders.BlobBuilder;
import be.ehealth.business.mycarenetdomaincommons.builders.BlobBuilderFactory;
import be.ehealth.businessconnector.mycarenet.agreement.validator.AgreementXmlValidatorImpl;
import be.ehealth.business.mycarenetcommons.v3.mapper.BlobMapper;
import be.ehealth.businessconnector.mycarenet.agreement.exception.AgreementBusinessConnectorExceptionValues;
import be.cin.encrypted.BusinessContent;
import be.cin.encrypted.EncryptedKnownContent;
import be.ehealth.technicalconnector.service.keydepot.KeyDepotManagerFactory;
import be.ehealth.technicalconnector.service.keydepot.KeyDepotManager.EncryptionTokenType;
import be.ehealth.technicalconnector.utils.ConnectorXmlUtils;
import be.ehealth.technicalconnector.utils.SessionUtil;
import be.ehealth.businessconnector.mycarenet.agreement.security.AgreementEncryptionUtil;
import org.apache.commons.codec.binary.Base64;
import be.fgov.ehealth.mycarenet.commons.protocol.v3.SendRequestType;
import be.ehealth.technicalconnector.exception.TechnicalConnectorException;
import be.ehealth.technicalconnector.exception.TechnicalConnectorExceptionValues;
import be.ehealth.business.mycarenetcommons.v3.mapper.RoutingMapper;
import be.fgov.ehealth.mycarenet.commons.core.v3.CommonInputType;
import be.ehealth.business.mycarenetdomaincommons.domain.CommonInput;
import be.ehealth.businessconnector.ehbox.api.domain.DocumentMessage;
import be.fgov.ehealth.ehbox.consultation.protocol.v3.Message;
import sophia.ehealth.SophiaSTSService;
import sophia.ehealth.SophiaCrypto;


public class JavaGateway {
  private static final Logger LOG = LoggerFactory.getLogger(JavaGateway.class);

  public SophiaSTSService getSophiaSTSService(){
    return new SophiaSTSService();
  }

  public static void main(String[] args) throws Exception {
    JavaGateway app = new JavaGateway();
    // app is now the gateway.entry_point
    GatewayServer server = new GatewayServer(app);
    System.out.println("Started");
    server.start();
  }

  public ConfigValidator getConfigValidator(){
    return ConfigFactory.getConfigValidator();
  }

  public ArrayList<SAMLAttributeDesignator> createAttributeDesignatorList(){
    // This causes issues if done outside Java program due to type conversion
    return new ArrayList<SAMLAttributeDesignator>();
  }

  public ArrayList<SAMLAttribute> createSAMLAttributeList(){
    // This causes issues if done outside Java program due to type conversion
    return new ArrayList<SAMLAttribute>();
  }

  public SAMLAttribute createSAMLAttribute(String v1, String v2, String v3) {
    // This causes issues if done outside Java program due to type conversion
    return new SAMLAttribute(v1, v2, v3);
  }

  public Map<String, Object> createHashMap(){
    return new HashMap<String, Object>();
  }

  public AttributeQuery createAttributeQueryFromTemplate(Map<String, Object> testFileParams, String requestLocation) throws Exception {
      return FileTestUtils.toObject(testFileParams, requestLocation, AttributeQuery.class);
  }

  public CommonInputMapper getCommontInputMapper(){
    return Mappers.getMapper(
                CommonInputMapper.class
            );
  }

  public MsgQuery newMsgQuery(){
    return new MsgQuery();
  }

  public be.cin.nip.async.generic.Query newQuery(){
    return new be.cin.nip.async.generic.Query();
  }

  public DocumentMessage<Message> createEmptyDocumentMessage(){
    return new DocumentMessage<Message>();
  }

  public ConfirmResponse confirmMessage(OrigineType origin, GenAsyncService service, byte[] hashValue) throws URISyntaxException, TechnicalConnectorException, GenAsyncBusinessConnectorException, SessionManagementException {
      List<byte[]> msgHashValues = new ArrayList<byte[]>();
      msgHashValues.add(hashValue);

      WsAddressingHeader responseConfirmHeader = new WsAddressingHeader(new URI("urn:be:cin:nip:async:generic:confirm:hash"));
      responseConfirmHeader.setTo(new URI(""));
      responseConfirmHeader.setFaultTo("http://www.w3.org/2005/08/addressing/anonymous");
      responseConfirmHeader.setReplyTo("http://www.w3.org/2005/08/addressing/anonymous");
      responseConfirmHeader.setMessageID(new URI(IdGeneratorFactory.getIdGenerator("uuid").generateId()));

      Confirm request = new Confirm();
      request.setOrigin(origin);
      request.getMsgHashValues().addAll(msgHashValues);
      ConfirmResponse confirmResponse = service.confirmRequest(request, responseConfirmHeader);
      return confirmResponse;
  }

    public ConfirmResponse confirmTAckMessage(OrigineType origin, GenAsyncService service, byte[] hashValue) throws URISyntaxException, TechnicalConnectorException, GenAsyncBusinessConnectorException, SessionManagementException {
      List<byte[]> tackHashValues = new ArrayList<byte[]>();
      tackHashValues.add(hashValue);

      WsAddressingHeader responseConfirmHeader = new WsAddressingHeader(new URI("urn:be:cin:nip:async:generic:confirm:hash"));
      responseConfirmHeader.setTo(new URI(""));
      responseConfirmHeader.setFaultTo("http://www.w3.org/2005/08/addressing/anonymous");
      responseConfirmHeader.setReplyTo("http://www.w3.org/2005/08/addressing/anonymous");
      responseConfirmHeader.setMessageID(new URI(IdGeneratorFactory.getIdGenerator("uuid").generateId()));

      Confirm request = new Confirm();
      request.setOrigin(origin);
      request.getTAckContents().addAll(tackHashValues);
      ConfirmResponse confirmResponse = service.confirmRequest(request, responseConfirmHeader);
      return confirmResponse;
  }

  public List commonInputAttributes(int attemptNbr) {
    return Arrays.asList(
        Attribute.builder()
                .key("urn:be:cin:nippin:attemptNbr")
                .value(attemptNbr)
                .build());
  }

  public byte[] getBytesFromFile(String path) throws Exception{
          return ConnectorIOUtils.getResourceAsString(path).getBytes(StandardCharsets.UTF_8);
  }

  public <T> ConfirmResponse confirmEAgreementMessage(String ref) throws ConnectorException {
      Confirm confirm = new Confirm();
      String projectName = "eagreement";
      McnPackageInfo packageInfo = McnConfigUtil.retrievePackageInfo("genericasync." + projectName);
      CommonBuilder commonBuilder = RequestBuilderFactory.getCommonBuilder(projectName);
      confirm.setOrigin(((CommonInputMapper)Mappers.getMapper(CommonInputMapper.class)).map(commonBuilder.createOrigin(packageInfo)));
      confirm.getMsgRefValues().add(ref);
      return GenAsyncSessionServiceFactory.getGenAsyncService(projectName).confirmRequest(confirm, WsAddressingUtil.createHeader(null, "urn:be:cin:nip:async:generic:confirm:hash"));
  }

  public EncryptedRequestObjectBuilderImplWithRouting getEncryptedRequestObjectBuilderImplWithRouting() {
    return new EncryptedRequestObjectBuilderImplWithRouting();
  }
  public class EncryptedRequestObjectBuilderImplWithRouting extends EncryptedRequestObjectBuilderImpl {
    public AskAgreementBuilderRequest buildAskAgreementRequest(boolean isTest, boolean altRouting, InputReference reference, Patient patientInfo, DateTime refDate, byte[] messageFHIR) throws TechnicalConnectorException, AgreementBusinessConnectorException {
        AskAgreementBuilderRequest requestBuilder = new AskAgreementBuilderRequest();
        this.build(isTest, reference, patientInfo, refDate, messageFHIR, requestBuilder);
        return requestBuilder;
    }
    private void checkParameterNotNull(Object references, String parameterName) throws AgreementBusinessConnectorException {
      if (references == null) {
         throw new AgreementBusinessConnectorException(AgreementBusinessConnectorExceptionValues.PARAMETER_NULL, new Object[]{parameterName});
      }
   }

   public <T extends AgreementBuilderRequest> void build(boolean isTest, boolean altRouting, InputReference references, Patient patientInfo, DateTime refDate, byte[] messageFHIR, T requestBuilder) throws TechnicalConnectorException, AgreementBusinessConnectorException {
      this.checkParameterNotNull(references, "InputReference");
      this.checkParameterNotNull(references.getInputReference(), "Input reference");
      String detailId = "_" + IdGeneratorFactory.getIdGenerator("uuid").generateId();
      BlobBuilder blobBuilder = BlobBuilderFactory.getBlobBuilder("agreement");
      BusinessContent businessContent = new BusinessContent();
      businessContent.setId(detailId);
      businessContent.setValue(messageFHIR);
      requestBuilder.setBusinessContent(businessContent);
      EncryptedKnownContent encryptedKnownContent = new EncryptedKnownContent();
      encryptedKnownContent.setReplyToEtk(KeyDepotManagerFactory.getKeyDepotManager().getETK(EncryptionTokenType.HOLDER_OF_KEY).getEncoded());
      encryptedKnownContent.setBusinessContent(businessContent);
      encryptedKnownContent.setXades(buildXades(detailId, ConnectorXmlUtils.toByteArray(businessContent)));
      if (LOG.isDebugEnabled()) {
         ConnectorXmlUtils.dump(encryptedKnownContent);
      }

      Object var11 = null;

      byte[] payload;
      try {
         payload = (new AgreementEncryptionUtil()).handleEncryption(encryptedKnownContent, SessionUtil.getHolderOfKeyCrypto());
         if (payload != null && ConfigFactory.getConfigValidator().getBooleanProperty("be.ehealth.businessconnector.mycarenet.agreement.builders.impl.dumpMessages", false)) {
            LOG.debug("EncryptedRequestObjectBuilder : Created blob content: " + Base64.encodeBase64String(payload));
         }
      } catch (Exception var15) {
         throw new TechnicalConnectorException(TechnicalConnectorExceptionValues.ERROR_CRYPTO, var15, new Object[0]);
      }

      Blob blob = blobBuilder.build(payload, "none", detailId, "text/xml", (String)null, "encryptedForKnownBED");
      SendRequestType request = requestBuilder.getRequest();
      CommonBuilder commonBuilder = RequestBuilderFactory.getCommonBuilder("agreement");
      
      request.setCommonInput(((be.ehealth.business.mycarenetcommons.v3.mapper.CommonInputMapper)Mappers.getMapper(be.ehealth.business.mycarenetcommons.v3.mapper.CommonInputMapper.class)).map(commonBuilder.createCommonInput(McnConfigUtil.retrievePackageInfo("agreement"), isTest, references.getInputReference())));
      if (altRouting){
        request.setRouting(((RoutingMapper)Mappers.getMapper(RoutingMapper.class)).map(commonBuilder.createRoutingToMutuality(patientInfo.getMutuality(), refDate)));
      } else {
        request.setRouting(((RoutingMapper)Mappers.getMapper(RoutingMapper.class)).map(commonBuilder.createRouting(patientInfo, refDate)));
      }
      request.setId(IdGeneratorFactory.getIdGenerator("xsid").generateId());
      request.setIssueInstant(new DateTime());
      request.setDetail(BlobMapper.mapBlobTypefromBlob(blob));
      (new AgreementXmlValidatorImpl()).validate(request);
   }

  }

}