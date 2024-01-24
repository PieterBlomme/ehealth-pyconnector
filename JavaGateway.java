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

public class JavaGateway {
  private static final Logger LOG = LoggerFactory.getLogger(JavaGateway.class);

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

  public Query newQuery(){
    return new Query();
  }

  public ConfirmResponse confirmTheseMessages(OrigineType origin, GenAsyncService service, GetResponse responseGet) throws URISyntaxException, TechnicalConnectorException, GenAsyncBusinessConnectorException, SessionManagementException {
      List<byte[]> msgHashValues = new ArrayList<byte[]>();
      for (MsgResponse msgResp : responseGet.getReturn().getMsgResponses()) {
          final byte[] hashValue = msgResp.getDetail().getHashValue();
          LOG.debug("adding confirm for msg hash >" + hashValue + "<");
          msgHashValues.add(hashValue);
      }

      List<byte[]> tackHashValues = new ArrayList<byte[]>();
      for (TAckResponse tackResponse : responseGet.getReturn().getTAckResponses()) {
          final byte[] hashValue = tackResponse.getTAck().getValue();
          LOG.debug("adding confirm for tack hash >" + hashValue + "<");
          tackHashValues.add(hashValue);
      }

      WsAddressingHeader responseConfirmHeader = new WsAddressingHeader(new URI("urn:be:cin:nip:async:generic:confirm:hash"));
      responseConfirmHeader.setTo(new URI(""));
      responseConfirmHeader.setFaultTo("http://www.w3.org/2005/08/addressing/anonymous");
      responseConfirmHeader.setReplyTo("http://www.w3.org/2005/08/addressing/anonymous");
      responseConfirmHeader.setMessageID(new URI(IdGeneratorFactory.getIdGenerator("uuid").generateId()));

      Confirm request = new Confirm();
      request.setOrigin(origin);
      request.getMsgHashValues().addAll(msgHashValues);
      request.getTAckContents().addAll(tackHashValues);
      ConfirmResponse confirmResponse = service.confirmRequest(request, responseConfirmHeader);
      return confirmResponse;
  }
  public List commonInputAttributes() {
    return Arrays.asList(Attribute.builder()
                .key("urn:be:cin:nippin:purpose")
                .value("some purpose")
                .build(),
        Attribute.builder()
                .key("urn:be:cin:nippin:attemptNbr")
                .value(1)
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

}